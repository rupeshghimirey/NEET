from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class AppointmentAll:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
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
    def save_appointment_all(cls,data):
        query = "INSERT INTO appointments_all (first_name, last_name, phone_number, date, time, created_at, updated_at) VALUES(%(first_name)s,%(last_name)s,%(phone_number)s,%(date)s,%(time)s, NOW(), NOW());"
        results =  connectToMySQL("neet_users_appointments").query_db(query,data)
        return results