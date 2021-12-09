from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import book
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'python_project_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
    
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for r in results:
            users.append(cls(r))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    # Users Pages 
    @ classmethod
    def get_one_user(cls, data):
        query = "SELECt * FROM users LEFT JOIN books ON user_id = users.id WHERE users.id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        for row in results:
            book_data = {
                'id':row['books.id'],
                'title':row['title'],
                'author':row['author'],
                'note':row['note'],
                'category':row['category'],
                'user_id':row['user_id'],
                'created_at':row['books.created_at'], 
                'updated_at':row['books.updated_at'], 
            }
            user.books.append(book.Book(book_data))
        return user
    
    @staticmethod 
    def is_valid_registration(user):
        is_valid = True 
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) > 1:
            flash('This email is already taken, please enter another', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('This email is invalid', 'registration')
            is_valid = False
        if len(user['first_name']) < 3:
            flash('Your first name must be at least 3 characters long', 'registration')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Your last name must be at least 3 characters long', 'registration')
            is_valid = False
        if len(user['password']) < 8:
            flash('Your password must be at least 8 characters long', 'registration')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('The password you entered does not match up', 'registration')
        if len(user['password']) < 1:
            flash('Password required')
            is_valid = False
        return is_valid