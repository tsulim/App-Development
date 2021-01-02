from Application import app
from flask import Flask, render_template, request, redirect, url_for
import shelve
from Forms import SearchForm
from BookOrder import *
from Order import *

@app.route('/search', methods=['GET','POST'])
def search():
    # searchform = SearchForm(request.form)
    if request.method == 'POST':

        search = request.form['search']

        # searchform.search.data = search

        bookDict = {}
        db = shelve.open('productstorage.db','r')
        bookDict = db['Books']
        db.close()

        searchresults = []
        for id in bookDict:
            book = bookDict.get(id)
            if search.lower() in book.get_bookName().lower():
                searchresults.append(book)
            elif search.lower() in book.get_author().lower():
                searchresults.append(book)
            elif search == "":
                searchresults.append(book)


        return render_template('searchresults.html', search = search, searchresults=searchresults)

    return render_template('searchresults.html')
