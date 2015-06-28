from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from mturides import db


usertrips = db.Table('usertrips',
		db.Column('uid', db.Integer, db.ForeignKey('user.id')),
		db.Column('rid', db.Integer, db.ForeignKey('ride.id')),
		)

class User(db.Model):
	__tablename__='user'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(64))
	google_id = db.Column(db.Integer())
	rides = db.relationship('Ride', secondary=usertrips,backref="passengers", lazy='dynamic')
	def hostRide(self, dest):
		newRide = Ride()
		newRide.host_id = self.id
		newRide.destination = dest
		self.rides.append(newRide)
		db.session.add(newRide)
		db.session.commit()
		return newRide

	def joinRide(self, ride):
		self.rides.append(ride)
		return self

	def bailRide(self, ride):
		self.rides.remove(ride)
		return self

	def getHostedRides(self):
		return Ride.query.filter(Ride.host_id==self.id)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True
	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r' % (self.name)

class Ride(db.Model):
	__tablename__='ride'
	id = db.Column(db.Integer(), primary_key=True)
	destination = db.Column(db.String(64))
	host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	applications = db.relationship('Application', backref="ride")
	def __repr__(self):
		return '<Ride to %r' % (self.destination)

	def getHost(self):
		return User.query.filter(User.id == self.host_id).first()

	def getPassengers(self):
		p = User.query.join(usertrips,(usertrips.c.uid == User.id)).filter(usertrips.c.rid==self.id)
		return p

	def getApplications(self):
		a=Application.query.filter(Application.host_id == self.id).all()
		print a
		return a

	def addApplication(self, application):
		self.applications.append(application)
		db.session.add(application)
		db.session.commit()
		return

class Application(db.Model):
	__tablename__='application'
	id = db.Column(db.Integer(), primary_key=True)
	acknowledged = db.Column(db.Integer())
	approved = db.Column(db.Integer())
	ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'))
	host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	messages = db.relationship('Message', backref="application")
	def __repr__(self):
		return '<Application for ride %r' % (self.id)

	def getApplicant(self):
		return User.query.filter(User.id == self.applicant_id).first()
	
	def getRide(self):
		return Ride.query.filter(Ride.id == self.ride_id).first()

	def getPassengers(self):
		p = User.query.join(usertrips,(usertrips.c.uid == User.id)).filter(usertrips.c.rid==self.id)
		return p

	def addMessage(self, newMessage):
		self.messages.append(newMessage)
		db.session.add(newMessage)
		db.session.commit()
		return

class Message(db.Model):
	__tablename__='message'
	id = db.Column(db.Integer(), primary_key=True)
	application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	text = db.Column(db.String(128))
