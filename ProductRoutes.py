from Application import app
from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateBookForm
import shelve, Book

import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, flash

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Secret Key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def retrieveFiles():
    entries = os.listdir(app.config['UPLOAD_FOLDER'])
    fileList = []
    for entry in entries:
        fileList.append(entry)
    return fileList



@app.route('/products/', methods=['GET','POST'])
def product():
    if request.method == 'POST':
        filter = request.form['filter']
        bookDict = {}
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']
        productdb.close()

        bookList = []
        for key in bookDict:
            book = bookDict.get(key)
            if filter == "Fiction" or filter == "Non-Fiction":
                if book.get_genre() == filter:
                    bookList.append(book)
            elif filter == "LowtoHigh" or "HightoLow":
                bookList.append(book)
                def byPrice_key(book):
                    return book.get_price()

                if filter == "LowtoHigh":
                    bookList = sorted(bookList, key=byPrice_key)
                elif filter == "HightoLow":
                    bookList = sorted(bookList, key=byPrice_key, reverse=True)

        return render_template('products.html',bookList=bookList)
    else:
        bookDict = {}
        try:
            productdb = shelve.open('productstorage.db', 'r')
            bookDict = productdb['Books']
            productdb.close()
        except:
            print('productstorage.db not found')

        bookList = []
        for key in bookDict:
            book = bookDict.get(key)
            bookList.append(book)
        return render_template('products.html', bookList=bookList, count=len(bookList))

@app.route('/createBook', methods=['GET', 'POST'])
def createBook():
    createBookForm = CreateBookForm(request.form)
    if request.method == 'POST' and createBookForm.validate():

        # Image
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # added uuid to make the filename unique. Otherwise, file with same names will override.
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + filename))

            filedir = str(uuid.uuid4()) + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filedir))

        bookDict = {}
        productdb = shelve.open('productstorage.db', 'c')
        try:
            bookDict = productdb['Books']
            currentID = productdb['currentID']
        except:
            print("Error in retrieving Books from storage.db.")
            currentID = 0

        book = Book.Book(createBookForm.bookName.data, createBookForm.author.data, createBookForm.price.data, createBookForm.genre.data, createBookForm.stock.data, createBookForm.summary.data, filedir, currentID)
        bookDict[book.get_bookID()] = book
        currentID = book.get_bookID()

        productdb['Books'] = bookDict
        productdb['currentID'] = currentID

        return redirect(url_for('retrieveBooks'))
    return render_template('createBook.html', form=createBookForm)

@app.route('/retrieveBooks')
def retrieveBooks():
    bookDict = {}
    try:
        productdb = shelve.open('productstorage.db', 'r')
        bookDict = productdb['Books']
        productdb.close()
    except:
        print('Error in retrieving from productstorage.db')

    bookList = []
    for key in bookDict:
        book = bookDict.get(key)
        bookList.append(book)
    return render_template('retrieveBooks.html', bookList=bookList, count=len(bookList))

@app.route('/updateBook/<int:id>/', methods=['GET', 'POST'])
def updateBook(id):
    updateBookForm = CreateBookForm(request.form)
    if request.method == 'POST' and updateBookForm.validate():

        bookDict = {}
        productdb = shelve.open('productstorage.db', 'w')
        bookDict = productdb['Books']

        book = bookDict.get(id)

        # Image
        # check if the post request has the file part
        if 'file' in request.files:

            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            # if file.filename == '':
            #     flash('No selected file')
            #     return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

            # added uuid to make the filename unique. Otherwise, file with same names will override.
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + filename))

                filedir = str(uuid.uuid4()) + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filedir))
                book.set_image(filedir)

        book.set_bookName(updateBookForm.bookName.data)
        book.set_author(updateBookForm.author.data)
        book.set_price(updateBookForm.price.data)
        book.set_genre(updateBookForm.genre.data)
        book.set_stock(updateBookForm.stock.data)
        book.set_summary(updateBookForm.summary.data)

        productdb['Books'] = bookDict
        productdb.close()

        return redirect(url_for('retrieveBooks'))

    else:
        bookDict = {}
        productdb = shelve.open('productstorage.db', 'r')
        bookDict = productdb['Books']
        productdb.close()

        book = bookDict.get(id)
        updateBookForm.bookName.data = book.get_bookName()
        updateBookForm.author.data = book.get_author()
        updateBookForm.price.data = book.get_price()
        updateBookForm.genre.data = book.get_genre()
        updateBookForm.stock.data = book.get_stock()
        updateBookForm.summary.data = book.get_summary()

    return render_template('updateBook.html', form=updateBookForm)

@app.route('/deleteBook/<int:id>', methods=['POST'])
def deleteBook(id):
     bookDict = {}
     productdb = shelve.open('productstorage.db', 'w')
     bookDict = productdb['Books']
     bookDict.pop(id)
     productdb['Books'] = bookDict
     productdb.close()
     return redirect(url_for('retrieveBooks'))
