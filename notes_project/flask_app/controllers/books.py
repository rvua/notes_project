from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.book import Book

@app.route('/books')
def book_dashboard():
    if 'user_id' not in session:
        return redirect('/log_in')
    all_books = Book.get_books_with_users()
    return render_template('list_book.html', all_books=all_books)

@app.route('/books/new')
def new_book():
    if 'user_id' not in session:
        return redirect('log_in')
    users = User.get_users()
    return render_template('new_book.html', users=users)

@app.route('/create_book', methods = ['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect('/log_in')
    if Book.is_valid(request.form):
        data = {
            'title':request.form['title'],
            'author':request.form['author'],
            'note':request.form['note'],
            'category':request.form['category'],
            'user_id':session['user_id']
        }
        Book.create_book(data)
        return redirect('/books')
    else:
        return redirect('/books/new')
    
@app.route('/books/<int:book_id>/edit')
def edit_book(book_id):
    if 'user_id' not in session:
        return redirect('/log_in')
    users = User.get_users()
    data = {
        'book_id':book_id 
    }
    book = Book.get_one_book(data)
    return render_template('edit_book.html', users = users, book = book)

@app.route('/update_book/<int:book_id>', methods=['POST'])
def update_book(book_id):
    if 'user_id' not in session:
        return redirect('/log_in')
    if Book.is_valid(request.form):
        data = {
            'book_id': book_id,
            'title':request.form['title'],
            'author':request.form['author'],
            'note':request.form['note'],
            'category':request.form['category'],
            'user_id':session['user_id']
        }
        Book.updated_book_info(data)
        return redirect('/books')
    else:
        return redirect(f'/books/{book_id}/edit')

@app.route('/books/<int:book_id>/delete')
def delete_book(book_id):
    if 'user_id' not in session:
        return redirect('/log_in')
    data = {
        'book_id':book_id
    }
    Book.delete_one_book(data)
    return redirect('/books')