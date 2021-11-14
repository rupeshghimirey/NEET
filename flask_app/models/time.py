from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Time:
    def __init__(self, data):
        self.id = data['id']
        self.time = data['time']


    @classmethod
    def get_all_times(cls):
        
        query = "SELECT * FROM times"
        result = connectToMySQL('neet_users_appointments').query_db( query);

        times = []

        for time in result:
            times.append(cls(time))
        return times