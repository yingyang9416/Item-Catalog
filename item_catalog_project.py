from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Library, Book, User

# imports for step5 Gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# New imports for this step
from flask import session as login_session
import random
import string

from flask import \
     Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

CLIENT_ID = \
    json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Library Books Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///librarybookswithuser.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # render the login template
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('\
                    Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    # This no longer used:  login_session['credentials'] = credentials
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    print credentials

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it does not, create a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
                150px;-webkit-border-radius: 150px;\
                -moz-border-radius: 150px;">'
    flash("you are now logged in as %s, user id: %s"
          % (login_session['username'],
             login_session['user_id']))
    print "done!"
    print login_session
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    libraries = session.query(Library).order_by(asc(Library.name))
    access_token = login_session.get('access_token')
    # access_token = login_session.get('credentials')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = \
            make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print login_session
        # return response
        return render_template('libraries.html', libraries=libraries)
    else:
        response = make_response(json.dumps('Failed \
                    to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
    	return response


# JSON APIs to view Restaurant Information
@app.route('/library/<int:library_id>/books/JSON')
def libraryBooksJSON(library_id):
    library = session.query(Library).filter_by(id=library_id).one()
    books = session.query(Book).filter_by(library_id=library_id).all()
    return jsonify(Books=[book.serialize for book in books])


@app.route('/library/<int:library_id>/books/<int:book_id>/JSON')
def booksJSON(library_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@app.route('/library/JSON')
def libraryJSON():
    libraries = session.query(Library).all()
    return jsonify(libraries=[l.serialize for l in libraries])


# Show all libraries
@app.route('/')
@app.route('/library/')
def showLibraries():
    libraries = session.query(Library).order_by(asc(Library.name))
    # print session
    return render_template('libraries.html', libraries=libraries)


# Create a new library
@app.route('/library/new/', methods=['GET', 'POST'])
def newLibrary():
    # Check if the user is loged in
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newLibrary = Library(name=request.form['name'], 
                             user_id=login_session['user_id'])
        session.add(newLibrary)
        flash('New Library %s Successfully Created' % newLibrary.name)
        session.commit()
        return redirect(url_for('showLibraries'))
    else:
        return render_template('newLibrary.html')


# Edit a library
@app.route('/library/<int:library_id>/edit/', methods=['GET', 'POST'])
def editLibrary(library_id):
    editedLibrary = session.query(Library).filter_by(id=library_id).one()
    # Check if the user is loged in
    if 'email' not in login_session:
        return redirect('/login')
    # Check if the user is the creator of the library
    if editedLibrary.user_id != login_session['user_id']:
        flash('You are not authorized to edit this library. \
                Please create your own library.')
        return redirect(url_for('showBooks', library_id=library_id))
    if request.method == 'POST':
        if request.form['name']:
            editedLibrary.name = request.form['name']
            flash('Library Successfully Edited -- %s' % editedLibrary.name)
            session.commit()
            return redirect(url_for('showBooks', library_id=library_id))
    else:
        return render_template('editLibrary.html', library=editedLibrary)


# Delete a library
@app.route('/library/<int:library_id>/delete/', methods=['GET', 'POST'])
def deleteLibrary(library_id):
    libraryToDelete = session.query(Library).filter_by(id=library_id).one()
    # Check if the user is loged in
    if 'email' not in login_session:
        return redirect('/login')
    # Check if the user is the creator of the library
    if libraryToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this library. \
            Please create your own library.')
        return redirect(url_for('showBooks', library_id=library_id))
    if request.method == 'POST':
        session.delete(libraryToDelete)
        flash('%s Successfully Deleted ' % libraryToDelete.name)
        session.commit()
        return redirect(url_for('showLibraries'))
    else:
        return render_template('deleteLibrary.html', library=libraryToDelete)


# Show library books
@app.route('/library/<int:library_id>/')
@app.route('/library/<int:library_id>/books/')
def showBooks(library_id):
    library = session.query(Library).filter_by(id=library_id).one()
    books = session.query(Book).filter_by(library_id=library_id).all()
    user = session.query(User).filter_by(id=library.user_id).one()
    return render_template('books.html', 
                           books=books, library=library, user=user)


# Create a new book
@app.route('/library/<int:library_id>/books/new/', methods=['GET', 'POST'])
def newBook(library_id):
    library = session.query(Library).filter_by(id=library_id).one()
    # Check if the user is loged in
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBook = Book(name=request.form['name'],
                       description=request.form['description'],
                       author=request.form['author'],
                       published_year=request.form['published_year'],
                       library_id=library_id,
                       user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        flash('New Book %s Successfully Created' % (newBook.name))
        return redirect(url_for('showBooks', library_id=library_id))
    else:
        return render_template('newBook.html', library_id=library_id)


# Edit a book


@app.route('/library/<int:library_id>/books/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBook(library_id, book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    library = session.query(Library).filter_by(id=library_id).one()
    # Check if the user is loged in
    if 'email' not in login_session:
        return redirect('/login')
    # Check if the user is the creator of the book
    if editedBook.user_id != login_session['user_id']:
        flash('You are not authorized to edit this book. \
            Please create your own book.')
        return redirect(url_for('showBooks', library_id=library_id))
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['author']:
            editedBook.author = request.form['author']
        if request.form['published_year']:
            editedBook.published_year = request.form['published_year']
        if request.form['description']:
            editedBook.description = request.form['description']
        flash('Successfully edited')
        session.commit()
        return redirect(url_for('showBooks', library_id=library_id))
    else:
        return render_template('editBooks.html',
                               library_id=library_id,
                               book_id=book_id, book=editedBook)


# Delete book


@app.route('/library/<int:library_id>/books/<int:book_id>/delete',
           methods=['GET', 'POST'])
def deleteBook(library_id, book_id):
    library = session.query(Library).filter_by(id=library_id).one()
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    # Check if the user is loged in
    if 'email' not in login_session:
        return redirect('/login')
    # Check if the user is the creator of the book or the library
    if login_session['user_id'] != bookToDelete.user_id \
       and login_session['user_id'] != library.user_id:
        flash('You are not authorized to delete this book. \
            Please create your own book.')
        return redirect(url_for('showBooks', library_id=library_id))
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        flash('Book Successfully Deleted')
        return redirect(url_for('showBooks', library_id=library_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete,
                               library_id=library_id)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
