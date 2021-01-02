from wtforms import Form, StringField, DecimalField, IntegerField, validators, ValidationError


class Quantity(Form):
    # booktitle = StringField('Book Title', [validators.Length(min=1,max=150), validators.DataRequired()])
    # bookprice = DecimalField('Book Price', [validators.NumberRange(min=0)])
    quantity = IntegerField('', [validators.NumberRange(min=0)])
