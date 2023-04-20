import os
import psycopg2
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
import json
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_migrate import Migrate

database_name = "medapp"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = "postgres:///{}".format(database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()
app = Flask(__name__)
#db = SQLAlchemy(app)

def setup_db(app):
    app.config.from_object('config')
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migration = Migrate(app, db)
    db.create_all()
    csrf = CSRFProtect(app)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    appo_day = db.Column(db.String(120), nullable=False)
    appo_time = db.Column(db.String(20), nullable=False)
    appo_available = db.Column(db.Boolean, nullable=False, default=True)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=False)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    
    def __repr__(self):
      return f'<appointment {self.id} {self.appo_day} {self.appo_time} {self.appo_available} doctor_appo_id {self.doctor_id}, patient_appo_id {self.patient_id}>'

    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'appo_day': self.appo_day,
            'appo_time': self.appo_time
        }    
    '''

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120))
    twiter_link = db.Column(db.String(120))
    linkedin_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    specialities = db.Column(db.String(120),nullable=False)
    upcoming_appo = db.Column(db.Integer, default=0)
    past_appo = db.Column(db.Integer, default=0)
    doctor = db.relationship('Appointment', backref='doctor_appo_id', lazy=True) 
    
    def __repr__(self):
      return f'<doctor {self.id} {self.name} {self.gender} {self.address} {self.city} {self.state} {self.phone} {self.appo_location} {self.facebook_link} {self.twiter_link} {self.linkedin_link} {self.website_link} {self.specialities} {self.upcoming_appo_count} {self.past_appo_count}>'
    
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'name': self.appo_day,
            'phone': self.phone,
            'facebook_link': self.facebook_link,
            'twiter_link': self.twiter_link,
            'linkedin_link': self.linkedin_link,
            'website_link': self.website_link,
            'specialities': self.specialities
        }    
    '''
        
class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.String(120), nullable=False)
    health_insurance_provider = db.Column(db.String(120))
    health_insurance_id = db.Column(db.String(120))
    seeking_specialities = db.Column(db.String(120),nullable=False)
    concern_description = db.Column(db.String(150),nullable=False)
    upcoming_appo = db.Column(db.Integer, default=0)
    past_appo = db.Column(db.Integer, default=0)
    patient = db.relationship('Appointment', backref='patient_appo_id', lazy=True) 
    
    def __repr__(self):
      return f'<patient {self.id} {self.name} {self.gender} {self.address} {self.city} {self.state} {self.phone} {self.appo_location} {self.date_of_birth} {self.health_insurance_provider} {self.health_insurance_id} {self.seeking_specialities} {self.upcoming_appo_count} {self.past_appo_count} >'
    
    '''
    def __repr__(self):
      return f'<doctor {self.id} {self.name} {self.gender} {self.address} {self.city} {self.state} {self.phone} {self.appo_location} {self.facebook_link} {self.twiter_link} {self.linkedin_link} {self.website_link} {self.specialities} {self.upcoming_appo_count} {self.past_appo_count}>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'name': self.appo_day,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth,
            'health_insurance_provider': self.health_insurance_provider,
            'health_insurance_id': self.health_insurance_id,
            'seeking_specialities': self.seeking_specialities,
            'concern_description': self.concern_description
        } 
    '''   


"""class Doctor_Rating(db.Model):
    __tablename__ = 'doctor_rating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    response_date = db.Column(db.DateTime, nullable=False)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=False)
    
    def __repr__(self):
      return f'<doctor_rating {self.id} {self.rating} {self.response_date} doctor_appo_id {self.doctor_id}>'   
    """


