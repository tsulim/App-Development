from flask import render_template, request, redirect, url_for, flash
from Application import app, db, bcrypt
from UserForms import RegistrationForm, LoginForm, UpdateAccountForm, DeleteUserForm
from models import User
from flask_login import login_user, current_user, logout_user
import shelve

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstName=form.firstName.data, address=form.address.data ,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            # Xiu Jia's Code    -   Move guest's cart into user's cart
            DictOngoingOrderDict = {}
            DictsaveforlaterDict = {}
            try:
                orderdb = shelve.open('orderstorage.db','w')
            except:
                print('Error in opening orderstorage.db')

            try:
                DictOngoingOrderDict = orderdb['OngoingOrder']
            except:
                print('Error in retrieving from orderdb')
            ongoingorderDict = DictOngoingOrderDict.get(0)

            try:
                DictsaveforlaterDict = orderdb['SaveForLater']
            except:
                print('Error in retrieving from orderdb')
            saveforlaterDict = DictsaveforlaterDict.get(0)

            if saveforlaterDict != {} or saveforlaterDict != None:
                usersaveforlater = DictsaveforlaterDict.get(current_user.id)
                if usersaveforlater == {} or usersaveforlater == None:
                    DictsaveforlaterDict[current_user.id] = saveforlaterDict
                else:
                    for key in saveforlaterDict:
                        item = saveforlaterDict.get(key)
                        usersaveforlater[key] = item
                    DictsaveforlaterDict[current_user.id] = usersaveforlater

                saveforlaterDict = {}
                DictsaveforlaterDict[0] = saveforlaterDict
                orderdb['SaveForLater'] = DictsaveforlaterDict


            if ongoingorderDict == None or ongoingorderDict == {}:
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                DictOngoingOrderDict[current_user.id] = ongoingorderDict
                ongoingorderDict = {}
                DictOngoingOrderDict[0] = ongoingorderDict
                orderdb['OngoingOrder'] = DictOngoingOrderDict
                orderdb.close()
                return redirect(url_for('checkout'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
    return render_template('settings.html', title='settings', form=form)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    form = DeleteUserForm()
    if form.validate_on_submit():
        found_user = User.query.filter_by(email=form.email.data).first()
        if found_user:
            user = User.query.filter_by(id=found_user.id).first()
            db.session.delete(user)
            db.session.commit()
            logout_user()
            return redirect(url_for('home'))
        else:
            flash('Delete Unsuccessful. Please check email', 'danger')
    return render_template('Delete.html', title='Delete', form=form)
