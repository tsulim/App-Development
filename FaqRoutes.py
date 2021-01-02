from Application import app
from flask import Flask, render_template, request, redirect, url_for
import shelve, FaqUser
from Forms import CreateUserForm
from flask_login import current_user


def descend(counter):
    return counter.get_counter()

@app.route('/faq')
def faq():
    faq = shelve.open('faq.db', 'c')

    if len(faq) > 0:
        mobile = {}
        basic = {}
        account = {}
        payment = {}
        privacy = {}
        delivery = {}
        mlist = []
        blist = []
        alist = []
        palist = []
        prlist = []
        dlist = []
        toplist =[]
        try:
            mobile = faq['M']
        except:
            print('Error in retrieving dict')
        for key in mobile:
            mlist.append(mobile.get(key))
        if mlist != []:
            mlist.sort(key=descend, reverse=True)
            toplist.append(mlist[0])
            print(toplist)

        try:
            basic = faq['B']
        except:
            print('Error in retrieving dict')
        for key in basic:
            blist.append(basic.get(key))
        if blist != []:
            blist.sort(key=descend, reverse=True)
            toplist.append(blist[0])

        try:
            account = faq['A']
        except:
            print('Error in retrieving dict')
        for key in account:
            alist.append(account.get(key))
        if alist != []:
            alist.sort(key=descend, reverse=True)
            toplist.append(alist[0])

        try:
            payment = faq['Pay']
        except:
            print('Error in retrieving dict')
        for key in payment:
            palist.append(payment.get(key))
        if palist != []:
            palist.sort(key=descend, reverse=True)
            toplist.append(palist[0])

        try:
            privacy = faq['Pri']
        except:
            print('Error in retrieving dict')
        for key in privacy:
            prlist.append(privacy.get(key))
        if prlist != []:
            prlist.sort(key=descend, reverse=True)
            toplist.append(prlist[0])


        try:
            delivery = faq['D']
        except:
            print('Error in retrieving dict')
        for key in delivery:
            dlist.append(delivery.get(key))
        if dlist != []:
            dlist.sort(key=descend, reverse=True)
            toplist.append(dlist[0])

        return render_template('faq.html',toplist=toplist, mobile=mlist, basic=blist, account=alist, payment=palist, privacy=prlist, delivery=dlist)
    else:
        return render_template('faq.html')




@app.route('/createQn', methods=['GET', 'POST'])
def createQn():
     if current_user.is_authenticated:
         createUserForm = CreateUserForm(request.form)
         if request.method == 'POST':
             faq = shelve.open('faq.db','c')
             qndict = {}
             user = FaqUser.User(createUserForm.firstName.data, createUserForm.lastName.data, createUserForm.topic.data, createUserForm.question.data)
             if user.get_topic() == 'M':
                 try:
                     qndict = faq['M']
                 except:
                     print("Error in retrieving Users from storage.db.")

                 qndict[user.get_question()] = user
                 faq['M'] = qndict
                 faq.close()

             elif user.get_topic() == 'B':
                 try:
                     qndict = faq['B']
                 except:
                     print("Error in retrieving Users from storage.db.")

                 qndict[user.get_question()] = user
                 faq['B'] = qndict
                 faq.close()

             elif user.get_topic() == 'A':
                 try:
                     qndict = faq['A']
                 except:
                     print("Error in retrieving Users from storage.db.")

                 qndict[user.get_question()] = user
                 faq['A'] = qndict
                 faq.close()

             elif user.get_topic() == 'Pay':
                 try:
                     qndict = faq['Pay']
                 except:
                     print("Error in retrieving Users from storage.db.")

                 qndict[user.get_question()] = user
                 faq['Pay'] = qndict
                 faq.close()

             elif user.get_topic() == 'Pri':
                 try:
                     qndict = faq['Pri']
                 except:
                     print("Error in retrieving Users from storage.db.")

                 qndict[user.get_question()] = user
                 faq['Pri'] = qndict

                 faq.close()

             elif user.get_topic() == 'D':
                 try:
                     qndict = faq['D']
                 except:
                     print("Error in retrieving Users from storage.db.")

                 qndict[user.get_question()] = user
                 faq['D'] = qndict

                 faq.close()


             return redirect(url_for('faq'))
         else:
              createUserForm.firstName.data = current_user.username

              return render_template('contact.html', form=createUserForm)
     else:
         return render_template('denied.html')


@app.route('/update/<qn>')
def update(qn):
    try:
        faq = shelve.open('faq.db', 'c')
        for key in faq:
            for x in faq[key]:
                a = x[:-1]
                if x == qn or a == qn:
                    if faq[key][x].get_firstName() == current_user.username or current_user.email == 'admin@admin.com':
                        show = faq[key][x]
                    else:
                        return render_template('denied.html')
        faq.close()
        return render_template('updateQn.html', qndetail=show)
    except:
        return render_template('denied.html')


@app.route('/ans/<qn>')
def ans(qn):

        if current_user.is_authenticated:
            faq = shelve.open('faq.db', 'c')
            for key in faq:
                for x in faq[key]:
                    a = x[:-1]
                    if x == qn or a == qn:
                        ans = faq[key][x]
                        attach = current_user.username

                        return render_template('ansQn.html', ansdetail=ans, attach=attach)
            faq.close()
            return 'ok'
        else:
            return render_template('denied.html')

@app.route('/update/test', methods=['POST'])
def test():
    qn = request.get_json(force=True)
    print(qn)
    faq = shelve.open('faq.db','w')
    dict = {}
    update = str(qn[4]) + ' (edited)'
    dict = faq[qn[3]]
    user = dict.get(qn[5])

    user.set_firstName(qn[0])
    user.set_lastName(qn[1])
    user.set_topic(qn[3])
    user.set_question(update)

    faq[qn[3]] = dict

    faq.close()
    return 'ok'


@app.route('/ans/lol', methods=['POST'])
def lol():
    if current_user.is_authenticated:
        ans = request.get_json(force=True)
        ansdb = shelve.open('ansdb.db','c')
        faq = shelve.open('faq.db','c')
        fullname = str(ans[0]) + ' ' + str(ans[1])
        list = [fullname, ans[3]]
        if ans[4] in ansdb:

            text = ansdb[ans[4]]
            text.append(list)
            ansdb[ans[4]] = text

        else:
            ansdb[ans[4]] = [list]
        dict = {}
        dict = faq[ans[2]]
        user = dict.get(ans[4])

        user.set_ans(ansdb[ans[4]])
        faq[ans[2]] = dict
        ansdb.close()

        faq.close()

        return redirect(url_for('faq'))


@app.route('/deleteqn/<qn>')
def deleteqn(qn):
        faq = shelve.open('faq.db', 'c')
        dict = {}
        for key in faq:
            for x in faq[key]:
                a = x[:-1]
                if x == qn or a == qn:
                    try:
                        if faq[key][x].get_firstName() == current_user.username or current_user.email == 'admin@admin.com':
                            dict = faq[key]
                            dict.pop(x)

                            faq[key] = dict
                            faq.close()
                            return redirect(url_for('faq'))
                        else:
                            return render_template('denied.html')
                    except:
                        return render_template('denied.html')
        return 'ok'


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/thanks2')
def thanks2():
    return render_template('thanks2.html')

@app.route('/upvote/<qn>')
def upvote(qn):
        if current_user.is_authenticated:
            faq = shelve.open('faq.db', 'c')
            dict = {}
            for key in faq:
                for x in faq[key]:
                    a = x[:-1]
                    if x == qn or a == qn:
                        if current_user.email == 'admin@admin.com':
                            dict = faq[key]
                            user = dict.get(x)
                            current = user.get_counter()
                            new = current[0] + 10
                            current[0] = new
                            user.set_counter(current)

                            faq[key] = dict
                        else:
                            if faq[key][x].get_firstName() != current_user.username:
                                dict = faq[key]
                                user = dict.get(x)
                                current = user.get_counter()
                                update = current[0]

                                current[0] = int(update) + 1
                                name = str(current_user.username)+'upvote'
                                name2 = str(current_user.username)+'downvote'
                                for x in current:
                                    if x == name:
                                        print(current)
                                        current[0] = int(update)
                                        user.set_counter = current
                                        return render_template('denied.html')
                                    elif x == name2:
                                        down = int(update) + 2

                                        current[0] = down
                                        current.remove(x)
                                current.append(name)
                                print(current)
                                user.set_counter(current)
                                faq[key] = dict
                            else:
                                print('same user bruh')
                                return render_template('denied.html')
            faq.close()

            return redirect(url_for('faq'))
        else:
            return render_template('denied.html')

@app.route('/downvote/<qn>')
def downvote(qn):
        if current_user.is_authenticated:
            faq = shelve.open('faq.db', 'c')
            dict = {}
            for key in faq:
                for x in faq[key]:
                    a = x[:-1]
                    if x == qn or a == qn:
                        if current_user.email == 'admin@admin.com':
                            dict = faq[key]
                            user = dict.get(x)
                            current = user.get_counter()
                            new = current[0] - 10
                            if new >= 0:
                                current[0] = new
                                user.set_counter(current)

                                faq[key] = dict
                            else:
                                current[0] = 0
                                user.set_counter(current)
                                faq[key] = dict
                        else:
                            if faq[key][x].get_firstName() != current_user.username:
                                dict = faq[key]
                                user = dict.get(x)
                                current = user.get_counter()
                                update = current[0]

                                current[0] = int(update) - 1
                                name = str(current_user.username) + 'upvote'
                                name2 = str(current_user.username) + 'downvote'
                                for x in current:
                                    if x == name2:
                                        current[0] = int(update)
                                        user.set_counter = current
                                        return render_template('denied.html')
                                    elif x == name:
                                        up = int(update) - 2
                                        if up < 0:
                                            current[0] = 0
                                        else:
                                            current[0] = up
                                        current.remove(x)
                                current.append(name2)
                                print(current)
                                if update >= 0:
                                    user.set_counter(current)
                                    faq[key] = dict
                                else:
                                    current[0] = 0
                                    user.set_counter(current)
                                    faq[key] = dict
                            else:
                                return render_template('denied.html')
            faq.close()

            return redirect(url_for('faq'))
        else:
            return render_template('denied.html')
