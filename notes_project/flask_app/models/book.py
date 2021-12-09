from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user 

class Book:
    db = 'python_project_schema'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.note = data['note']
        self.category = data['category']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}

    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books (title, author, note, category, user_id, created_at, updated_at) VALUES (%(title)s, %(author)s, %(note)s, %(category)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod 
    def get_books_with_users(cls):
        query = "SELECT * FROM books LEFT JOIN users ON user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        books = []
        for row in results:
            book = cls(row)
            user_data = {
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            book.user = user.User(user_data)
            books.append(book)
        return books 
    
    @classmethod
    def get_one_book(cls, data):
        query = "SELECT * FROM books LEFT JOIN users ON user_id = users.id WHERE books.id = %(book_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        book = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        book.user = user.User(user_data)
        return book 
        
    @classmethod 
    def updated_book_info(cls, data):
        query = "UPDATE books SET title = %(title)s, author = %(author)s, note = %(note)s, category = %(category)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(book_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    
    @classmethod
    def delete_one_book(cls, data):
        query = "DELETE FROM books WHERE id = %(book_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    
    @staticmethod
    def is_valid(book):
        is_valid = True
        if len(book['title']) == 0:
            is_valid = False
            flash('You must enter a title')
        if len(book['title']) < 3:
            is_valid = False
            flash('Please enter correct title')
        if book['author'] == '':
            is_valid = False
            flash('Author required')
        if book['category'] == '':
            is_valid = False
            flash('Please choose a category') 
        return is_valid
    
