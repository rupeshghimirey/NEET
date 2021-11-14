from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Appointment:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.user_id = data['user_id']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = [];

    @staticmethod
    def validate_appointment(form_data):
        is_valid = True
        if (len(form_data['first_name'])) < 1:
            flash("Please enter your name")
            is_valid = False;
        if (len(form_data['last_name'])) < 1:
            flash("Please put your last name!")
            is_valid = False;
        if (len(form_data['phone_number'])) < 10:
            flash("Please put a valid phone number!")
            is_valid = False;
        if (len(form_data['date'])) < 10:
            flash("Please put a valid phone date!")
            is_valid = False;
        if (len(form_data['time'])) < 1:
            flash("Please enter a valid time!")
            is_valid = False;
        
        return is_valid

    @classmethod
    def save_appointment(cls,data):
        query = "INSERT INTO appointments (first_name, last_name, phone_number, date, time, user_id, created_at, updated_at) VALUES(%(first_name)s,%(last_name)s,%(phone_number)s,%(date)s,%(time)s,%(user_id)s, NOW(), NOW());"
        results =  connectToMySQL("neet_users_appointments").query_db(query,data)
        return results
    @classmethod
    def save_appointment_all(cls,data):
        query = "INSERT INTO appointments_all (first_name, last_name, phone_number, date, time, created_at, updated_at) VALUES(%(first_name)s,%(last_name)s,%(phone_number)s,%(date)s,%(time)s, NOW(), NOW());"
        results =  connectToMySQL("neet_users_appointments").query_db(query,data)
        return results

    @classmethod
    def get_all_appointments_with_user(cls,data):
        
        query = "SELECT * FROM appointments LEFT JOIN users on users.id = appointments.user_id WHERE users.id = %(user_id)s "
        result = connectToMySQL('neet_users_appointments').query_db( query,data);

        all_appointments = []
        for row in result:
            one_appointment = cls(row)

            user_data = {
            "id" : row["users.id"],
            "first_name"  : row["first_name"],
            "last_name"   : row["last_name"],
            "email"         : row["email"],
            "password"         : row["password"],
            "created_at"  : row["users.created_at"],
            "updated_at"  : row["users.updated_at"]
            }

            one_appointment.user = User(user_data)
            all_appointments.append(one_appointment)
        return all_appointments

    @classmethod
    def get_one_appointment_with_user(cls,data):
        query = "SELECT * FROM appointments LEFT JOIN users on users.id = appointments.user_id WHERE appointments.id = %(appointment_id)s "
        result = connectToMySQL('neet_users_appointments').query_db( query, data);

        appointment = cls(result[0])

        user_data = {
            "id" : result[0]["users.id"],
            "first_name"  : result[0]["first_name"],
            "last_name"   : result[0]["last_name"],
            "email"         : result[0]["email"],
            "password"         : result[0]["password"],
            "created_at"  : result[0]["users.created_at"],
            "updated_at"  : result[0]["users.updated_at"]
            }
        
        appointment.user = User(user_data)

        return appointment;



    @classmethod
    def update_appointment(cls,data):
        query = "UPDATE appointments SET first_name = %(first_name)s, last_name = %(last_name)s, phone_number = %(phone_number)s, date = %(date)s, time = %(time)s, user_id = %(user_id)s WHERE id = %(appointment_id)s"
        
        connectToMySQL('neet_users_appointments').query_db( query, data )
    @classmethod
    def delete_appointment(cls,data):
        query = "DELETE FROM appointments WHERE id = %(appointment_id)s"
        connectToMySQL('neet_users_appointments').query_db( query, data)