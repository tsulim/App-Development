from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, DateField, ValidationError, Field
from wtforms.fields.html5 import EmailField, TelField, SearchField
from datetime import *


class CreateBookForm(Form):
    bookName = StringField('Book Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    author = StringField('Author', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price', [validators.DataRequired()])
    genre = SelectField('Genre', [validators.DataRequired()], choices=[('', 'Select'), ('Non-Fiction', 'Non-Fiction'), ('Fiction', 'Fiction')], default='')
    stock = StringField('Stock', [validators.DataRequired()])
    summary = TextAreaField('Summary', [validators.Optional()])

def validate_card(form, field):
    if len(str(field.data)) == 16:
        if str(field.data)[0] == 4:
            pass
        elif str(field.data)[0] == 5:
            pass
        else:
            raise ValidationError('Invalid Credit Card Number')
    else:
        raise ValidationError('Invalid Credit Card Number')


class CheckoutForm(Form):
    cardtype = SelectField('Card Type', validators=[validators.DataRequired()], choices=[('','Select'),('Visa','Visa'),('MasterCard','MasterCard'),('AmericanExpress','American Express')], default='')
    cardnumber = StringField('Card Number', validators=[validators.DataRequired()])
    expirydate = DateField('Expiry Date', validators=[validators.DataRequired()], format='%m/%Y', render_kw={"placeholder": "MM/YYYY"})
    CVV = StringField('CVV', validators=[validators.DataRequired(), validators.Length(min=3,max=3)])
    firstName = StringField('First Name', validators=[validators.Length(min=1,max=150), validators.DataRequired()])
    lastName = StringField('Last Name', validators=[validators.Length(min=1,max=150), validators.DataRequired()])
    country = StringField('Country', validators=[validators.DataRequired()])
    address = StringField('Address', validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.DataRequired()])
    state = StringField('State', validators=[validators.optional()])
    zipcode = StringField('ZIP Code', validators=[validators.DataRequired()])
    mobile = TelField('Mobile Number', validators=[validators.DataRequired()])
    email = EmailField('Email Address', validators=[validators.DataRequired(),validators.Email()])


    def validate_cardnumber(self,cardnumber):
        # if len(cardnumber.data) == 16:
        #     if self.cardtype.data == "Visa":
        #         if cardnumber.data.startwith('4'):
        #             pass
        #         else:
        #             raise ValidationError('Invalid Visa Number!')
        #     elif self.cardtype.data == "MasterCard":
        #         if cardnumber.data.startwith('5'):
        #             pass
        #         else:
        #             raise ValidationError('Invalid MasterCard Number')
        # elif len(cardnumber.data) == 15:
        #     if self.cardtype.data == "AmericanExpress":
        #         if cardnumber.data.startwith('3'):
        #             pass
        #         else:
        #             raise ValidationError('Invalid American Express Number')
        # else:
        #     raise ValidationError('Invalid Card Number!')
        if len(cardnumber.data) == 15 or len(cardnumber.data) == 16:
            pass
        else:
            raise ValidationError('Invalid Card Number!')


    def validate_expirydate(self,expirydate):
        currentDate = date.today()
        if currentDate > expirydate.data:
            raise ValidationError('Invalid Expiry Date')


class SearchForm(Form):
    search = StringField('', render_kw={"placeholder": "Search keyword and hit enter..."})

class CreateUserForm(Form):
     firstName = StringField('First Name', validators=[validators.Length(min=1,max=150), validators.DataRequired()])
     lastName = StringField('Last Name', validators=[validators.Length(min=1,max=150), validators.DataRequired()])
     topic = SelectField('Topic', validators=[validators.DataRequired()],choices=[('B', 'Basic'), ('M', 'Mobile'), ('A', 'Account'),('Pay', 'Payment'), ('Pri', 'Privacy'), ('D', 'Delivery')], default='B')
     question = TextAreaField('Question', validators=[validators.Optional(),validators.DataRequired()])

class AddressForm(Form):
    firstname = StringField('First Name', validators=[validators.Length(min=1, max=150), validators.DataRequired()])
    lastname = StringField('Last Name', validators=[validators.Length(min=1,max=150), validators.DataRequired()])
    address = StringField('Address', validators=[validators.DataRequired()])
    country = StringField('Country',validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.DataRequired()])
    state = StringField('State', validators=[validators.optional()])
    zipcode = StringField('ZIP Code/Postal Code', validators=[validators.DataRequired()])
    mobile = TelField('Mobile Number', validators=[validators.DataRequired()])
