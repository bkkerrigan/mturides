from . import app, googlelogin, db
from forms import HostRideForm
from models import User, Ride, Application, Message

from flask import render_template, redirect, url_for, request, jsonify
from flask.ext.login import login_required, login_user, current_user, logout_user

#View functions
@app.route('/')
@app.route('/index')
@login_required
def index():
	if current_user:
		print '----Hello ' + current_user.name +'----------'
	u = User.query.all()
	r = Ride.query.all()
	return render_template('index.html', users = u, rides= r, user = current_user)


@app.route('/hostRide', methods=['GET', 'POST'])
@login_required
def host():
	form = HostRideForm()
	if form.validate_on_submit():
		current_user.hostRide(form.destination.data)
		redirect(url_for('index'))
	return render_template('hostRide.html', form=form, user = current_user)

#r_id = ride_id
@app.route('/apply/<int:r_id>')
@login_required
def apply(r_id):
	ride = Ride.query.filter(Ride.id == r_id).first()
	application = Application.query.filter(Application.ride_id == r_id).filter(Application.applicant_id == current_user.id).first()

	if application is None:
		application = Application(ride_id=ride.id, applicant_id=current_user.id, host_id=ride.host_id, approved=False)
		ride.addApplication(application)
		
	return redirect(url_for('applying', a_id=application.id))


@app.route('/application/<int:a_id>')
@login_required
def applying(a_id):
	application = Application.query.filter(Application.id==a_id).first()
	h = User.query.filter(User.id == Application.host_id).first()
	a = User.query.filter(User.id == Application.applicant_id).first()

	return render_template('application.html', user = current_user,application=application, host=h, applicant=a)

@app.route('/refreshApplicaton/<int:a_id>', methods =['GET', 'POST'])
def refreshChat(a_id):
	application = Application.query.filter(Application.id==a_id).first()
	messages = Message.query.filter(Message.application_id==application.id).all()
	messageLog = []
	for m in messages:
		messageLog.append(str(str(m.author_id) + ': ' + str(m.text) + '\r'))

	print messageLog
	return jsonify(result = messageLog)

@app.route('/acceptApplication/<int:a_id>', methods=['GET', 'POST'])
@login_required
def acceptApplication(a_id):
	application = Application.query.filter(Application.id==a_id).first()

	if request.form['accept'] == "1":
		application.setApproval(True)
	else:
		application.setApproval(False)


	return jsonify(result = "")

@app.route('/postMessage/<int:a_id>', methods=['GET', 'POST'])
@login_required
def postMessage(a_id):
	application = Application.query.filter(Application.id==a_id).first()
	newMessage = Message(application_id = application.id, author_id = current_user.id, text=request.form['message'])
	application.addMessage(newMessage)
	return None

@app.route('/manageRides')
@login_required
def manage():
	for r in current_user.getHostedRides():
		for p in r.getPassengers():
			print p.name
	return render_template('manageRides.html', user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return render_template('logout.html')



@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
	print request.form['gid']

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **params):
	user = User.query.filter_by(google_id=userinfo['id']).first()
	if user:
		print()
	else:
		user = User(google_id=userinfo['id'],name=userinfo['name'])
		db.session.add(user)
		db.session.commit()
	login_user(user, remember=False)

	print str('WE ARE GOING BACK TO THE INDEX PAGE')
	return redirect(url_for('index'))

@googlelogin.user_loader
def load_user(id):
	return User.query.get(int(id))