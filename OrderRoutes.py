from Application import app
from flask import Flask, render_template, request, redirect, url_for, flash
from OrderForm import Quantity
import shelve
from Forms import CheckoutForm, AddressForm
from BookOrder import *
from Order import *
# from Book import *
from Address import Address
from flask_login import current_user
from fpdf import FPDF
import os
import uuid
from datetime import date

@app.route('/single/<int:id>', methods=['POST','GET'])
def addtoCart(id):
    quantity = Quantity(request.form)
    if request.method == 'POST' and quantity.validate():
        bookDict = {}
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']
        productdb.close()
        book = bookDict.get(id)
        stock = book.get_stock()

        if int(stock) < quantity.quantity.data:
            flash('Number must be between 0 and ' + str(stock), category='Quantity Error')
            return redirect(url_for('addtoCart', id=id))
        else:
            ongoingOrderDict = {}
            DictOngoingOrderDict = {}
            orderdb = shelve.open('orderstorage.db','c')

            try:
                DictOngoingOrderDict = orderdb['OngoingOrder']       # Retrieve Dict containing Ongoing Order Dict of all users
                if current_user.is_authenticated:
                    ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)    # Retrieve Ongoing Order Dict of current user
                else:
                    ongoingOrderDict = DictOngoingOrderDict.get(0)

            except:
                print('Error in retrieving Order from orderstorage.db.')

            if ongoingOrderDict == None:    # If User don't have a Ongoing Order
                ongoingOrderDict = {}

            if ongoingOrderDict.get(id) == None:

                bkOrder = BookOrder(book.get_bookName(), book.get_price(), quantity.quantity.data, book.get_image())
                bkOrder.set_orderbkID(id)
            else:
                bkOrder = ongoingOrderDict.get(id)
                currentquantity = bkOrder.get_quantity()
                currentquantity += quantity.quantity.data
                if int(stock) < currentquantity:
                    flash('Current Available Quantity: ' + stock + '<br>Quantity in Cart: ' + str(bkOrder.get_quantity()), category='Quantity Error')
                    return redirect(url_for('addtoCart', id=id))
                else:
                    bkOrder.set_quantity(currentquantity)


            ongoingOrderDict[id] = bkOrder
            if current_user.is_authenticated:
                DictOngoingOrderDict[current_user.id] = ongoingOrderDict
            else:
                DictOngoingOrderDict[0] = ongoingOrderDict
            orderdb['OngoingOrder'] = DictOngoingOrderDict

            orderdb.close()

            return redirect(url_for('cart'))

    else:
        bookDict = {}
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']

        book = bookDict.get(id)
        productdb.close()

        return render_template('shopsingle.html', form=quantity, defnum=1, book=book )

@app.route('/buynow/<int:id>', methods=["POST"])
def buynow(id):
    quantity = Quantity(request.form)
    if request.method == "POST" and quantity.validate():
        bookDict = {}
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']
        productdb.close()
        book = bookDict.get(id)
        stock = book.get_stock()

        if int(stock) < quantity.quantity.data:
            flash('Number must be between 0 and ' + str(stock), category='Quantity Error')
            return redirect(url_for('addtoCart', id=id))
        else:
            ongoingOrderDict = {}
            DictOngoingOrderDict = {}
            orderdb = shelve.open('orderstorage.db','c')

            try:
                DictOngoingOrderDict = orderdb['OngoingOrder']       # Retrieve Dict containing Ongoing Order Dict of all users
                if current_user.is_authenticated:
                    ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)    # Retrieve Ongoing Order Dict of current user
                else:
                    ongoingOrderDict = DictOngoingOrderDict.get(0)

            except:
                print('Error in retrieving Order from orderstorage.db.')

            if ongoingOrderDict == None:
                ongoingOrderDict = {}
                bookDict = {}
                productdb = shelve.open('productstorage.db','r')
                bookDict = productdb['Books']
                productdb.close()

                book = bookDict.get(id)

                bkOrder = BookOrder(book.get_bookName(), book.get_price(), quantity.quantity.data, book.get_image())
                bkOrder.set_orderbkID(id)

                ongoingOrderDict[id] = bkOrder
                if current_user.is_authenticated:
                    DictOngoingOrderDict[current_user.id] = ongoingOrderDict
                else:
                    DictOngoingOrderDict[0] = ongoingOrderDict
                orderdb['OngoingOrder'] = DictOngoingOrderDict

                orderdb.close()
            else:

                if ongoingOrderDict.get(id) == None:
                    bookDict = {}
                    productdb = shelve.open('productstorage.db','r')
                    bookDict = productdb['Books']
                    productdb.close()

                    book = bookDict.get(id)

                    bkOrder = BookOrder(book.get_bookName(), book.get_price(), quantity.quantity.data, book.get_image())
                    bkOrder.set_orderbkID(id)
                else:
                    bkOrder = ongoingOrderDict.get(id)
                    currentquantity = bkOrder.get_quantity()
                    currentquantity += quantity.quantity.data
                    book = bookDict.get(id)
                    stock = book.get_stock()
                    if int(stock) < currentquantity:
                        flash('Current Available Quantity: ' + stock + '<br>Quantity in Cart: ' + str(bkOrder.get_quantity()), category='Quantity Error')
                        return redirect(url_for('addtoCart', id=id))
                    else:
                        bkOrder.set_quantity(currentquantity)


                ongoingOrderDict[id] = bkOrder
                if current_user.is_authenticated:
                    DictOngoingOrderDict[current_user.id] = ongoingOrderDict
                else:
                    DictOngoingOrderDict[0] = ongoingOrderDict
                orderdb['OngoingOrder'] = DictOngoingOrderDict

                orderdb.close()

            return redirect(url_for('checkout'))

@app.route('/cart', methods=['POST','GET'])   #Retrieve Book Order
def cart():
    if request.method == 'POST':

        return redirect(url_for('checkout'))

    else:
        ongoingOrderDict = {}
        DictOngoingOrderDict = {}
        orderdb = {}
        try:
            orderdb = shelve.open('orderstorage.db','r')
        except:
            print('Error in retrieving from orderstorage.db')

        try:
            DictOngoingOrderDict = orderdb['OngoingOrder']
            if current_user.is_authenticated:
                ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
            else:
                ongoingOrderDict = DictOngoingOrderDict.get(0)
            orderdb.close()
        except:
            print('Error in retrieving Order from OngoingOrder')


        orderList = []
        overall_price = 0
        try:
            for key in ongoingOrderDict:
                book = ongoingOrderDict.get(key)
                orderList.append(book)
                overall_price += float(book.get_total_cost())
        except:
            print('Empty Ongoing Order Dict')

        return render_template('cart.html', orderList=orderList, overall_price=overall_price)

@app.route('/removeFromCart/<int:id>', methods=['GET'])
def removeFromCart(id):
    ongoingOrderDict = {}
    DictOngoingOrderDict = {}
    orderdb = shelve.open('orderstorage.db','w',writeback='True')
    DictOngoingOrderDict = orderdb['OngoingOrder']
    if current_user.is_authenticated:
        ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
    else:
        ongoingOrderDict = DictOngoingOrderDict.get(0)

    ongoingOrderDict.pop(id)

    if current_user.is_authenticated:
        DictOngoingOrderDict[current_user.id] = ongoingOrderDict
    else:
        DictOngoingOrderDict[0] = ongoingOrderDict
    orderdb['OngoingOrder'] = DictOngoingOrderDict
    orderdb.close()

    return redirect(url_for('cart'))

@app.route('/updateBookOrder/<int:id>', methods=['GET','POST'])
def updateBookOrder(id):
    updateBookOrderForm = Quantity(request.form)
    if request.method == 'POST' and updateBookOrderForm.validate():
        bookDict = {}
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']
        productdb.close()
        book = bookDict.get(id)
        stock = book.get_stock()

        if int(stock) < updateBookOrderForm.quantity.data:
            flash('Number must be between 0 and ' + str(stock), category='Quantity Error')
            return redirect(url_for('updateBookOrder', id=id))
        else:

            ongoingOrderDict = {}
            DictOngoingOrderDict = {}
            orderdb = shelve.open('orderstorage.db','w')
            DictOngoingOrderDict = orderdb['OngoingOrder']
            if current_user.is_authenticated:
                ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
            else:
                ongoingOrderDict = DictOngoingOrderDict.get(0)

            book = ongoingOrderDict.get(id)
            book.set_quantity(updateBookOrderForm.quantity.data)

            if current_user.is_authenticated:
                DictOngoingOrderDict[current_user.id] = ongoingOrderDict
            else:
                DictOngoingOrderDict[0] = ongoingOrderDict
            orderdb['OngoingOrder'] = DictOngoingOrderDict
            orderdb.close()

            return redirect(url_for('cart'))

    else:
        ongoingOrderDict = {}
        DictOngoingOrderDict = {}
        orderdb = shelve.open('orderstorage.db','r')
        DictOngoingOrderDict = orderdb['OngoingOrder']
        if current_user.is_authenticated:
            ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
        else:
            ongoingOrderDict = DictOngoingOrderDict.get(0)
        orderdb.close()

        bookDict = {}
        productdb = shelve.open('productstorage.db','r')
        bookDict = productdb['Books']
        productdb.close()


        bookdetail = bookDict.get(id)
        book = ongoingOrderDict.get(id)

        updateBookOrderForm.quantity.data = book.get_quantity()


        return render_template('updateBookOrder.html', form=updateBookOrderForm, book=book, bookdetail=bookdetail)


@app.route('/checkout', methods=['GET','POST'])
def checkout():
    checkoutform = CheckoutForm(request.form)
    if request.method == 'POST' and checkoutform.validate():

        ongoingOrderDict = {}
        DictOngoingOrderDict = {}
        orderdb = shelve.open('orderstorage.db','r')
        DictOngoingOrderDict = orderdb['OngoingOrder']
        ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
        orderdb.close()

        overall_price = 0
        orderList = []
        for key in ongoingOrderDict:
            book = ongoingOrderDict.get(key)
            overall_price += float(book.get_total_cost())
            orderList.append(book)

        # Deduct Stock with Quantity purchased
        bookDict = {}
        productdb = shelve.open('productstorage.db','w')
        bookDict = productdb['Books']

        for key in ongoingOrderDict:
            book = ongoingOrderDict.get(key)
            quantity = book.get_quantity()
            bookdetail = bookDict.get(key)
            currentquantity = int(bookdetail.get_stock())
            currentquantity -= int(quantity)
            bookdetail.set_stock(currentquantity)
            # Add Quantity Sold
            quantitysold = bookdetail.get_quantitysold()
            quantitysold += quantity
            bookdetail.set_quantitysold(quantitysold)
            bookDict[key] = bookdetail

        productdb['Books'] = bookDict


        # Move Ongoing Order Data to Completed Order db and del Ongoing db
        completedorderdict = {}
        DictCompletedOrderDict = {}
        DictOrdercurrentID = {}
        orderdb = shelve.open('orderstorage.db','w')

        try:
            DictCompletedOrderDict = orderdb['CompletedOrder']
            DictOrdercurrentID = orderdb['currentID']

            completedorderdict = DictCompletedOrderDict.get(current_user.id)
            currentID = DictOrdercurrentID.get(current_user.id)

        except:
            print('Error in retrieving Users from storage.db.')
            currentID = 0

        if currentID == None:
            currentID = 0

        if completedorderdict == None:
            completedorderdict = {}

        order = Order(ongoingOrderDict, currentID)

        deliveryID = str(current_user.id) + "a" + str(order.get_orderID())
        order.set_userID(current_user.id)
        order.set_deliveryID(deliveryID)
        order.set_paymentmethod(checkoutform.cardtype.data)
        order.set_date()
        order.set_time()
        address = checkoutform.address.data + " " + checkoutform.country.data + " " + checkoutform.zipcode.data
        order.set_address(address)
        order.set_overall_cost(overall_price)
        order.set_orderStatus('Processing')

        completedorderdict[order.get_orderID()] = order
        DictCompletedOrderDict[current_user.id] = completedorderdict
        orderdb['CompletedOrder'] = DictCompletedOrderDict

        currentID = order.get_orderID()
        DictOrdercurrentID[current_user.id] = currentID
        orderdb['currentID'] = DictOrdercurrentID

        ongoingOrderDict = {}

        DictOngoingOrderDict[current_user.id] = ongoingOrderDict
        orderdb['OngoingOrder'] = DictOngoingOrderDict

        DictAddressDict = {}
        AddressDict = {}
        addressdb = {}
        DictcurrentID = {}
        # Creating Address Storage
        try:
            addressdb = shelve.open('addressStorage.db','c')
        except:
            print('Error in opening addressStorage.db')
        # Retrieving Address Dict from Address Storage
        try:
            DictAddressDict = addressdb['Address']
            AddressDict = DictAddressDict.get(current_user.id)
        except:
            print('Empty Address Dict')

        try:
            DictcurrentID = addressdb['currentID']
            addresscurrentID = DictcurrentID.get(current_user.id)
        except:
            print('Empty Current Address ID dict')
            addresscurrentID = 0

        if addresscurrentID == None:
            addresscurrentID = 0
        # addressID = 0
        if AddressDict == None or AddressDict == {}:
            AddressDict = {}
            newaddress = Address(checkoutform.firstName.data,checkoutform.lastName.data, checkoutform.address.data, checkoutform.country.data, checkoutform.city.data, checkoutform.state.data, checkoutform.zipcode.data, checkoutform.mobile.data, addresscurrentID)
            AddressDict[newaddress.get_addressID()] = newaddress
            DictAddressDict[current_user.id] = AddressDict
            addressdb['Address'] = DictAddressDict

            addresscurrentID = newaddress.get_addressID()
            DictcurrentID[current_user.id] = addresscurrentID
            addressdb['currentID'] = DictcurrentID
        else:
            same = 0
            for key in AddressDict:
                address = AddressDict.get(key)
                if address.get_address() == checkoutform.address.data:
                    same += 1
                    addressID = address.get_addressID()

            if same < 1:
                firstname = checkoutform.firstName.data
                lastname = checkoutform.lastName.data
                newaddress = Address(firstname, lastname, checkoutform.address.data, checkoutform.country.data, checkoutform.city.data, checkoutform.state.data, checkoutform.zipcode.data, checkoutform.mobile.data, addresscurrentID)
                AddressDict[newaddress.get_addressID()] = newaddress
                DictAddressDict[current_user.id] = AddressDict
                addressdb['Address'] = DictAddressDict

                addresscurrentID = newaddress.get_addressID()
                DictcurrentID[current_user.id] = addresscurrentID
                addressdb['currentID'] = DictcurrentID

                addressID = addresscurrentID
        addressdb.close()
        orderdb.close()

        return redirect(url_for('receipt', id=currentID, addressID=addressID))
    else:
        ongoingOrderDict = {}
        DictOngoingOrderDict = {}
        orderdb = shelve.open('orderstorage.db','r')
        DictOngoingOrderDict = orderdb['OngoingOrder']
        ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
        orderdb.close()

        overall_price = 0
        orderList = []
        for key in ongoingOrderDict:
            book = ongoingOrderDict.get(key)
            overall_price += float(book.get_total_cost())
            orderList.append(book)


        if current_user.is_authenticated:
            checkoutform.email.data = current_user.email
            # checkoutform.address.data = current_user.address
            checkoutform.firstName.data = current_user.firstName

            # Retrieve Address Dict for current user
            DictAddressDict = {}
            AddressDict = {}
            addressdb = {}
            try:
                addressdb = shelve.open('addressStorage.db','r')
            except:
                print('Error in opening addressStorage.db')
            try:
                DictAddressDict = addressdb['Address']
                AddressDict = DictAddressDict.get(current_user.id)
                addressdb.close()
            except:
                print('Empty Address Dict')
            if AddressDict == None:
                AddressDict = {}
            AddressList = []
            for key in AddressDict:
                address = AddressDict.get(key)
                AddressList.append(address)


        return render_template('checkout.html', orderList=orderList, overall_price=overall_price, form=checkoutform, AddressList=AddressList)

@app.route('/checkout/<int:addressid>', methods=['POST'])
def changeaddress(addressid):
    checkoutform = CheckoutForm(request.form)
    try:
        addressdb = shelve.open('addressStorage.db','r')
    except:
        print('Error in opening addressStorage.db')

    try:
        DictAddressDict = addressdb['Address']
        AddressDict = DictAddressDict.get(current_user.id)
        addressdb.close()
    except:
        print('Empty Address Dict')

    address = AddressDict.get(addressid)
    checkoutform.firstName.data = address.get_firstname()
    checkoutform.lastName.data = address.get_lastname()
    checkoutform.address.data = address.get_address()
    checkoutform.country.data = address.get_country()
    checkoutform.city.data = address.get_city()
    checkoutform.state.data = address.get_state()
    checkoutform.zipcode.data = address.get_postalcode()
    checkoutform.mobile.data = address.get_mobile()

    ongoingOrderDict = {}
    DictOngoingOrderDict = {}
    orderdb = shelve.open('orderstorage.db','r')
    DictOngoingOrderDict = orderdb['OngoingOrder']
    ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
    orderdb.close()

    overall_price = 0
    orderList = []
    for key in ongoingOrderDict:
        book = ongoingOrderDict.get(key)
        overall_price += float(book.get_total_cost())
        orderList.append(book)

    checkoutform.email.data = current_user.email

    # Retrieve Address Dict for current user
    DictAddressDict = {}
    AddressDict = {}
    addressdb = {}
    try:
        addressdb = shelve.open('addressStorage.db','r')
    except:
        print('Error in opening addressStorage.db')
    try:
        DictAddressDict = addressdb['Address']
        AddressDict = DictAddressDict.get(current_user.id)
        addressdb.close()
    except:
        print('Empty Address Dict')

    AddressList = []
    for key in AddressDict:
        address = AddressDict.get(key)
        AddressList.append(address)


    return render_template('checkout.html', orderList=orderList, overall_price=overall_price, form=checkoutform, AddressList=AddressList)

@app.route('/thankyou/<pdfFilename>', methods=['GET'])
def thankyou(pdfFilename):
    return render_template('thankyou.html', pdfFilename=pdfFilename)

@app.route('/deleteaddress/<int:addressid>',methods=['GET','POST'])
def deleteaddress(addressid):
    addressdb = shelve.open('addressStorage.db','w')
    DictAddressDict = addressdb['Address']
    AddressDict = DictAddressDict.get(current_user.id)

    AddressDict.pop(addressid)

    DictAddressDict[current_user.id] = AddressDict
    addressdb['Address'] = DictAddressDict
    addressdb.close()

    return redirect(url_for('checkout'))

@app.route('/editaddress/<int:addressid>',methods=['GET','POST'])
def editaddress(addressid):
    addressform = AddressForm(request.form)
    if request.method == "POST":
        addressdb = shelve.open('addressStorage.db','w')
        DictAddressDict = addressdb['Address']
        AddressDict = DictAddressDict.get(current_user.id)
        address = AddressDict.get(addressid)

        address.set_firstname(addressform.firstname.data)
        address.set_lastname(addressform.lastname.data)
        address.set_address(addressform.address.data)
        address.set_country(addressform.country.data)
        address.set_city(addressform.city.data)
        address.set_state(addressform.state.data)
        address.set_postalcode(addressform.zipcode.data)
        address.set_mobile(addressform.mobile.data)

        AddressDict[addressid] = address
        DictAddressDict[current_user.id] = AddressDict
        addressdb['Address'] = DictAddressDict

        addressdb.close()
        return redirect(url_for('checkout'))
    else:
        addressdb = shelve.open('addressStorage.db','r')
        DictAddressDict = addressdb['Address']
        addressdb.close()

        AddressDict = DictAddressDict.get(current_user.id)
        address = AddressDict.get(addressid)

        addressform.firstname.data = address.get_firstname()
        addressform.lastname.data = address.get_lastname()
        addressform.address.data = address.get_address()
        addressform.country.data = address.get_country()
        addressform.city.data = address.get_city()
        addressform.state.data = address.get_state()
        addressform.zipcode.data = address.get_postalcode()
        addressform.mobile.data = address.get_mobile()


        return render_template('editaddress.html', form = addressform, addressid=addressid)

@app.route('/addtoLater/<int:id>', methods=['GET'])
def addtoLater(id):
    saveforlaterDict = {}
    ongoingOrderDict = {}
    DictsaveforlaterDict = {}
    DictOngoingOrderDict = {}
    orderdb = shelve.open('orderstorage.db','w')

    try:
        DictOngoingOrderDict = orderdb['OngoingOrder']
        if current_user.is_authenticated:
            ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
        else:
            ongoingOrderDict = DictOngoingOrderDict.get(0)
    except:
        print('Error in retrieving Order from orderstorage.db')

    try:
        DictsaveforlaterDict = orderdb['SaveForLater']
        if current_user.is_authenticated:
            saveforlaterDict = DictsaveforlaterDict.get(current_user.id)
        else:
            saveforlaterDict = DictsaveforlaterDict.get(0)
    except:
        print('Error in retrieving Saveforlater from orderstorage.db')

    if saveforlaterDict == None:
        saveforlaterDict = {}

    bookorder = ongoingOrderDict.get(id)

    saveforlaterDict[id] = bookorder
    if current_user.is_authenticated:
        DictsaveforlaterDict[current_user.id] = saveforlaterDict
    else:
        DictsaveforlaterDict[0] = saveforlaterDict

    orderdb['SaveForLater'] = DictsaveforlaterDict

    ongoingOrderDict.pop(id)

    if current_user.is_authenticated:
        DictOngoingOrderDict[current_user.id] = ongoingOrderDict
    else:
        DictOngoingOrderDict[0] = ongoingOrderDict
    orderdb['OngoingOrder'] = DictOngoingOrderDict

    orderdb.close()

    return redirect(url_for('saveforlater'))

@app.route('/saveforlater',methods=['GET'])
def saveforlater():
    saveforlaterDict = {}
    DictsaveforlaterDict = {}
    try:
        orderdb = shelve.open('orderstorage.db','r')
    except:
        print('Error in opening orderstorage.db')

    try:
        DictsaveforlaterDict = orderdb['SaveForLater']
        if current_user.is_authenticated:
            saveforlaterDict = DictsaveforlaterDict.get(current_user.id)
        else:
            saveforlaterDict = DictsaveforlaterDict.get(0)
        orderdb.close()
    except:
        print('Error in retrieving Dict from SaveForLater')

    saveforlaterlist = []
    try:
        for key in saveforlaterDict:
            book = saveforlaterDict.get(key)
            saveforlaterlist.append(book)

    except:
        print('Empty Save For Later Dict')

    return render_template('saveforlater.html', saveforlaterlist=saveforlaterlist)

@app.route('/movetocart/<int:id>', methods=['GET'])
def movetocart(id):
    saveforlaterDict = {}
    ongoingOrderDict = {}
    DictsaveforlaterDict = {}
    DictOngoingOrderDict = {}
    orderdb = shelve.open('orderstorage.db','w')

    try:
        DictOngoingOrderDict = orderdb['OngoingOrder']
        if current_user.is_authenticated:
            ongoingOrderDict = DictOngoingOrderDict.get(current_user.id)
        else:
            ongoingOrderDict = DictOngoingOrderDict.get(0)
    except:
        print('Error in retrieving Order from orderstorage.db')

    try:
        DictsaveforlaterDict = orderdb['SaveForLater']
        if current_user.is_authenticated:
            saveforlaterDict = DictsaveforlaterDict.get(current_user.id)
        else:
            saveforlaterDict = DictsaveforlaterDict.get(0)
    except:
        print('Error in retrieving Saveforlater from orderstorage.db')

    bookorder = saveforlaterDict.get(id)

    ongoingOrderDict[id] = bookorder
    if current_user.is_authenticated:
        DictOngoingOrderDict[current_user.id] = ongoingOrderDict
    else:
        DictOngoingOrderDict[0] = ongoingOrderDict

    orderdb['OngoingOrder'] = DictOngoingOrderDict

    saveforlaterDict.pop(id)
    if current_user.is_authenticated:
        DictsaveforlaterDict[current_user.id] = saveforlaterDict
    orderdb['SaveForLater'] = DictsaveforlaterDict

    orderdb.close()

    return redirect(url_for('cart'))

@app.route('/deletefromlist/<int:id>', methods=['GET'])
def deletefromlist(id):
    saveforlaterDict = {}
    DictsaveforlaterDict = {}
    orderdb = shelve.open('orderstorage.db','w',writeback='True')
    DictsaveforlaterDict = orderdb['SaveForLater']
    if current_user.is_authenticated:
        saveforlaterDict = DictsaveforlaterDict.get(current_user.id)
    else:
        saveforlaterDict = DictsaveforlaterDict.get(0)

    saveforlaterDict.pop(id)

    if current_user.is_authenticated:
        DictsaveforlaterDict[current_user.id] = saveforlaterDict
    else:
        DictsaveforlaterDict[0] = saveforlaterDict
    orderdb['SaveForLater'] = DictsaveforlaterDict
    orderdb.close()

    return redirect(url_for('saveforlater'))

@app.route('/receipt/<int:id>/<int:addressID>',methods=['GET'])
def receipt(id,addressID):
    CompletedOrderDict = {}
    DictCompletedOrderDict = {}
    try:
        orderdb = shelve.open('orderstorage.db','r')
    except:
        print('Error in opening orderstorage.db')

    try:
        DictCompletedOrderDict = orderdb['CompletedOrder']
        CompletedOrderDict = DictCompletedOrderDict.get(current_user.id)
    except:
        print('Empty Completed Order Dict')

    completedorder = CompletedOrderDict.get(id)

    bkorderDict = completedorder.get_orderdict()

    bkorderList = []
    for key in bkorderDict:
        bkorder = bkorderDict.get(key)
        bkorderList.append(bkorder)

    addressDict = {}
    DictAddressDict = {}
    try:
        addressdb = shelve.open('addressStorage.db','r')
    except:
        print('Error in opening addressStorage.db')

    try:
        DictAddressDict = addressdb['Address']
        addressDict = DictAddressDict.get(current_user.id)
    except:
        print('Error in retrieving Dict Address Dict')

    address = addressDict.get(addressID)

    # Creating PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', '', 13.0)

    pdf.set_line_width(0.0)
    pdf.rect(15.0, 15.0, 170.0, 245.0)

    pdf.image('static/images/logo.PNG', 20.0, 17.0, link='', type='', w=45.0, h=12.0)

    pdf.set_line_width(0.0)
    pdf.line(100.0, 15.0, 100.0, 57.0)

    pdf.set_font('arial', 'B', 14.0)
    pdf.set_xy(125.0, 25.5)
    pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt=completedorder.get_deliveryID(), border=0)

    pdf.set_xy(115.0, 27.5)
    pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='No: ', border=0)

    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(115.0, 33.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Date:', border=0)

    pdf.set_xy(135.0, 33.0)
    pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=str(date.today()), border=0)
    pdf.set_line_width(0.0)
    pdf.line(15.0, 57.0, 185.0, 57.0)

    pdf.set_font('times', '', 10.0)
    pdf.set_xy(17.0, 59.0)
    pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Mr/Mrs/Miss/Mdm:', border=0)

    pdf.set_xy(47.0, 59.0)
    pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=address.get_firstname() + " " + address.get_lastname(), border=0)

    pdf.set_xy(17.0, 64.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Address:', border=0)

    pdf.set_xy(35.0, 64.0)
    pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=address.get_address(), border=0)

    pdf.set_xy(17.0, 69.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Mobile:', border=0)

    pdf.set_xy(35.0, 69.0)
    pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=address.get_mobile(), border=0)

    pdf.set_xy(115.0, 69.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='City:', border=0)

    pdf.set_xy(133.0, 69.0)
    pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=address.get_city(), border=0)

    pdf.set_line_width(0.0)
    pdf.line(15.0, 77.0, 185.0, 77.0)

    pdf.set_line_width(0.0)
    pdf.line(120.0, 77.0, 120.0, 230.0)

    pdf.set_line_width(0.0)
    pdf.line(155.0, 77.0, 155.0, 230.0)

    pdf.set_xy(20.0, 79.0)
    pdf.cell(ln=0, h=5.0, align='L', w=125.0, txt='Item', border=0)

    pdf.set_xy(125.0, 79.0)
    pdf.cell(ln=0, h=5.0, align='C', w=20.0, txt='Quantity', border=0)

    pdf.set_xy(160.0, 79.0)
    pdf.cell(ln=0, h=5.0, align='R', w=20.0, txt='Amount', border=0)

    pdf.set_line_width(0.0)
    pdf.line(15.0, 86.0, 185.0, 86.0)

    textheight = 86.0
    lineheight = 93.0
    for item in bkorderList:

        pdf.set_xy(20.0, textheight)
        pdf.cell(ln=0, h=7.0, align='L', w=125.0, txt=item.get_title(), border=0)

        pdf.set_xy(125.0, textheight)
        pdf.cell(ln=0, h=7.0, align='C', w=20.0, txt=str(item.get_quantity()), border=0)


        pdf.set_xy(160.0, textheight)
        pdf.cell(ln=0, h=7.0, align='R', w=20.0, txt="$"+str(item.get_total_cost()), border=0)

        pdf.set_line_width(0.0)
        pdf.line(15.0, lineheight, 185.0, lineheight)

        textheight += 7
        lineheight += 7
        # 97+7

    # End for

    pdf.set_line_width(0.0)
    pdf.line(15.0, 230.0, 185.0, 230.0)

    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(105.0, 234.0)
    pdf.cell(ln=0, h=9.0, align='R', w=45.0, txt='Subtotal:', border=0)

    pdf.set_font('arial', 'B', 12.0)
    pdf.set_xy(145.0, 234.0)
    pdf.cell(ln=0, h=9.0, align='R', w=33.0, txt="$" + str(completedorder.get_overall_cost()), border=0)

    # Barcode
    pdf.interleaved2of5('012345678905', 20.0, 243.5, w=0.75)

    pdf.set_font('arial', 'B', 12.0)
    pdf.set_xy(105.0, 251.0)
    pdf.cell(ln=0, h=9.0, align='R', w=73.0, txt="$" + str(completedorder.get_overall_cost()), border=0)

    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(125.0, 251.0)
    pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)

    pdf.set_line_width(0.0)
    pdf.rect(155.0, 252.0, 25.0, 7.0)

    # Barcode number
    pdf.set_font('courier', '', 10.0)
    pdf.set_xy(20.0, 253.0)
    pdf.cell(ln=0, h=7.0, align='L', w=120.0, txt='012345678905', border=0)

    # filedir = 'invoice' + str(uuid.uuid4())
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filedir))
    pdf.close()
    pdfFilename = str(uuid.uuid4()) + "invoice.pdf"

    pdf.output(pdfFilename, 'F')

    # pdfFilename = str(uuid.uuid4()) + "invoice.pdf"
    # pdfDir = "static/pdfs/" + pdfFilename
    # pdf.output(pdfDir, 'F')

    return redirect(url_for('thankyou', pdfFilename = pdfFilename))

import webbrowser

@app.route('/viewreceipt/<pdfFilename>',methods=['GET'])
def viewreceipt(pdfFilename):
    # os.system(pdfFilename)
    webbrowser.open(pdfFilename+".pdf")
    return redirect(url_for('thankyou', pdfFilename=pdfFilename))

