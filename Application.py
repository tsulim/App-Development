from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@app.route('/', methods=['GET','POST'])
def home():

    # Codes to retrieve products and sort them into popular books and new books
    bookDict = {}
    try:
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']
        productdb.close()

    except:
        print('Error in opening productstorage.db')

    popularList = []
    newList = []
    bookList = []
    for key in bookDict:
        book = bookDict.get(key)
        if book.get_quantitysold() == 0 or book.get_bookID() > (len(bookDict)-5):
            newList.append(book)
        elif book.get_quantitysold() > 0:
            popularList.append(book)
        bookList.append(book)

    bookList.reverse()
    count = 0
    while count<5:
        for i in bookList:
            count+=1
            newList.append(i)

    # not done

    return render_template('home.html', popularList = popularList, newList = newList)

from UserRoutes import *
from SearchRoutes import *
from ProductRoutes import *
from OrderRoutes import *
from DeliveryRoutes import *
from FaqRoutes import *


if __name__ == '__main__':
    app.run()
