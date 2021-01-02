from Application import app
from flask import Flask, render_template, request, redirect, url_for
import shelve
from Delivery import *
from Status import *
from flask_login import current_user

@app.route('/history')
def history():
    ordersDict = {}
    DictOrderDict = {}
    try:
        orderdb = shelve.open('orderstorage.db', 'r')
        DictOrderDict = orderdb['CompletedOrder']
        ordersDict = DictOrderDict.get(current_user.id)
        orderdb.close()
    except:
        print("Error in retreiving from CompletedOrder")



    orderList = []
    if ordersDict != None:
        for key in ordersDict:
            singleOrder = ordersDict.get(key)
            orderList.append(singleOrder)
    return render_template('history.html', count=len(orderList), orderList=orderList)

@app.route('/historyDetails/<int:id>/')
def historyDetails(id):
    ordersDict = {}
    DictOrderDict = {}
    orderdb = shelve.open('orderstorage.db', 'r')
    DictOrderDict = orderdb['CompletedOrder']
    ordersDict = DictOrderDict.get(current_user.id)
    orderdb.close()

    bkorderDetails = []
    singleorder = ordersDict.get(id)
    orderdict = singleorder.get_orderdict()
    for key in orderdict:
        bkorder = orderdict.get(key)
        bkorderDetails.append(bkorder)

    deliveryDict = {}
    DictDeliveryDict = {}
    orderStatus = ""
    deliveryID = str(current_user.id) + "a" + str(id)
    try:
        deliverydb = shelve.open('statusStorage.db','r')   #to retrieve status line 39 to 46
        deliveryDict = deliverydb['delivery']
        delivery = deliveryDict.get(deliveryID)
        deliverydb.close()


        statusDict = delivery.get_statusDict()
        statusList = []
        for key in statusDict:
            status = statusDict.get(key)
            statusList.append(status)

    except:
        print('No status created yet!')
        statusList = None

    try:
        orderDict = {}
        DictOrderDict = {}
        orderdb = shelve.open('orderstorage.db', 'r')
        DictOrderDict = orderdb['CompletedOrder']
        orderDict = DictOrderDict.get(current_user.id)
        order = orderDict.get(id)
        orderStatus = order.get_orderStatus()    #to show on client side processing or delviering or delivered

        orderdb.close()


    except:
           print("Error for retreiving orderStatus for client side , line 63")

    return render_template('historyDetails.html', bkorderDetails=bkorderDetails, singleorder=singleorder, statusList=statusList, orderStatus=orderStatus)

@app.route('/delivery', methods=['GET' , 'POST'])
def delivery():
    if request.method == "POST": #to search for order number
        orderInput = request.form['orderInput']
        ordersDict = {}
        DictOrdersDict = {}
        requestedOrder = {}

        slice = orderInput.find('a')
        userID = int(orderInput[:slice])
        orderID = int(orderInput[slice+1:])

        try:
            orderdb = shelve.open('orderstorage.db','r')
            DictOrdersDict = orderdb['CompletedOrder']
            ordersDict = DictOrdersDict.get(userID)
            orderdb.close()
        except:
            print('Error in opening orderstorage.db')

        requestedOrder = ordersDict.get(orderID)

        return render_template('delivery.html',orderInput=orderInput, requestedOrder=requestedOrder)
    else:
        ordersDict = {}
        DictOrderDict = {}
        ListOrder = []
        try:
            orderdb = shelve.open('orderstorage.db','r')
            DictOrderDict = orderdb['CompletedOrder']
            orderdb.close()

        except:
            print('Error in opening orderstorage.db')

        for key in DictOrderDict:
            ordersDict = DictOrderDict.get(key)
            for i in ordersDict:
                order = ordersDict.get(i)
                ListOrder.append(order)
        def byDelivery_ID(order):
            return order.get_deliveryID()

        ListOrder = sorted(ListOrder, key=byDelivery_ID)

        return render_template('delivery.html', ListOrder=ListOrder)

@app.route('/deliveryUpdate/<orderInput>', methods=['GET' , 'POST'])   #CRUD -C, to create status
def deliveryUpdate(orderInput):
    if request.method == 'POST':

        slice = orderInput.find('a')
        userID = int(orderInput[:slice])
        orderID = int(orderInput[slice+1:])


        dropdownStatus = request.form['dropdownStatus']
        inputStatus = request.form['inputStatus']  #get input from status bar
        statusDict = {}
        statusList = []
        deliveryDict = {}

        DictStatuscurrentID = {}
        deliverydb = shelve.open('statusStorage.db','c')
        try:
            deliveryDict = deliverydb['delivery']
            retrieveDelivery = deliveryDict.get(orderInput)   #to retrieve specific object
            statusDict = retrieveDelivery.get_statusDict()

            for key in statusDict:
                status = statusDict.get(key)
                statusList.append(status)

            DictStatuscurrentID = deliverydb['currentID']
            currentID = DictStatuscurrentID.get(orderInput)
        except:
            print("Error in retrieving the data from shelve!")
            currentID = 0

        #     Set
        if inputStatus != None:
            status = Status(inputStatus,currentID)   #get the staff from the bar and run thru the damm class and then store in Status var
            statusDict[status.get_statusID()] = status

            delivery = objDelivery(orderInput,statusDict)
            deliveryDict[delivery.get_deliveryID()] = delivery
            deliverydb['delivery'] = deliveryDict

            DictStatuscurrentID[orderInput] = status.get_statusID()
            deliverydb['currentID'] = DictStatuscurrentID

            deliverydb.close()
            statusList.append(status)

        if dropdownStatus != None:    #update the radio buttons for order status in delivery Update
            orderDict = {}
            DictOrderDict = {}
            orderdb = shelve.open('orderstorage.db', 'w')
            DictOrderDict = orderdb['CompletedOrder']
            orderDict = DictOrderDict.get(userID)
            order = orderDict.get(orderID)

            order.set_orderStatus(dropdownStatus)

            orderDict[orderID] = order
            DictOrderDict[userID] = orderDict
            orderdb['CompletedOrder'] = DictOrderDict
            orderdb.close()

        return render_template('deliveryUpdate.html', statusList = statusList, deliveryDict=deliveryDict,Status=Status, orderInput=orderInput, dropdownStatus=dropdownStatus)
    else:    #this is the "GET" portion

        slice = orderInput.find('a')
        userID = int(orderInput[:slice])
        orderID = int(orderInput[slice+1:])

        statusDict = {}
        deliveryDict = {}

        dropdownStatus = ""
        deliverydb = {}
        try:
            deliverydb = shelve.open('statusStorage.db','r')
        except:
            print('No statusStorage.db')
        try:
            deliveryDict = deliverydb['delivery']   #to retrieve delivery objects
            retrieveDelivery = deliveryDict.get(orderInput)     # #to retrieve specific object
            statusDict = retrieveDelivery.get_statusDict()

            statusList = []
            for key in statusDict:
                status = statusDict.get(key)
                statusList.append(status)

        except:
            print("Error in retrieving the data from shelve!")
            statusList = None

        try:
            orderDict = {}
            DictOrderDict = {}
            orderdb = shelve.open('orderstorage.db', 'r')
            DictOrderDict = orderdb['CompletedOrder']
            orderDict = DictOrderDict.get(userID)
            order = orderDict.get(orderID)
            dropdownStatus = order.get_orderStatus()
            orderdb.close()
        except:
            print("error in opening orderstorage.db , line 155 got error la")

        return render_template('deliveryUpdate.html', statusList=statusList,orderInput=orderInput, userID = userID, orderID = orderID, dropdownStatus=dropdownStatus)


@app.route('/deleteStatus/<int:userID>/<int:orderID>/<int:statusID>/', methods=['POST','GET'])
def deleteStatus(userID,orderID,statusID):
    deliveryDict = {}
    orderInput = str(userID) + 'a' + str(orderID)
    deliverydb = shelve.open('statusStorage.db','w')
    deliveryDict = deliverydb['delivery']
    delivery = deliveryDict.get(orderInput)
    statusDict = delivery.get_statusDict()
    statusDict.pop(statusID)


    delivery.set_statusDict(statusDict)
    deliveryDict[orderInput] = delivery
    deliverydb['delivery'] = deliveryDict
    deliverydb.close()
    return redirect(url_for('deliveryUpdate', orderInput = orderInput, userID=userID, orderID=orderID))
