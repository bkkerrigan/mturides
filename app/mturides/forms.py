
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, validators

##use this form for the wtf_form(form) on the login page
class HostRideForm(Form):
	destination = StringField('Destination')
	submit = SubmitField('Create Ride')
