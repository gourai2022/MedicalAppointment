from datetime import datetime, date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL, Optional, Length
from models import *
from wtforms.fields import DateField,DateTimeField 

class AppointmentForm(FlaskForm):
    #days_show = date.today().isoformat() - (date.today()+timedelta(days=30)).isoformat() 
    #appo_day = DateTimeField('days_show', format='%m-%d-%Y' , validators=[DataRequired()])
    appo_day = DateField('appo_day', format='%Y-%m-%d' , validators=[DataRequired()])
        
    appo_time = SelectField(
        'appo_time', validators=[DataRequired()],
        choices=[
            ('09:30', '09:30'),
            ('10:30', '10:30'),
            ('11:30', '11:30'),
            ('01:30', '01:30'),
            ('02:30', '02:30'),
            ('03:30', '03:30'),
        ]
    )
    doctor_id = StringField(
        'doctor_id'
    )
    patient_id = StringField(
        'patient_id'
    )
    

class PatientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'), ])
    address = StringField('address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ])
    phone = StringField('phone', validators=[DataRequired()])
    #date_of_birth = DateTimeField('Date_of_birth', format='%m-%d-%Y', validators=[DataRequired()])
    date_of_birth = DateField('date_of_birth', format='%Y-%m-%d' , validators=[DataRequired()])
    health_insurance_provider = StringField('health_insurance_provider', validators=[DataRequired()])
    health_insurance_id = StringField('health_insurance_id', validators=[DataRequired()])
    seeking_specialities = SelectField('seeking_specialities', validators=[DataRequired()],
        choices=[
            ('Allergy and immunology', 'Allergy and immunology'),
            ('Dermatology', 'Dermatology'),
            ('Diagnostic radiology', 'Diagnostic radiology'),
            ('Emergency medicine', 'Emergency medicine'),
            ('Family medicine', 'Family medicine'),
            ('Internal medicine', 'Internal medicine'),
            ('Medical genetics', 'Medical genetics'),
            ('Neurology', 'Neurology'),
            ('Nuclear medicine', 'Nuclear medicine'),
            ('Obstetrics and gynecology', 'Obstetrics and gynecology'),
            ('Ophthalmology', 'Ophthalmology'),
            ('Pathology', 'Pathology'),
            ('Pediatrics', 'Pediatrics'),
            ('Physical medicine and rehabilitation', 'Physical medicine and rehabilitation'),
            ('Preventive medicine', 'Preventive medicine'),
            ('Psychiatry', 'Psychiatry'),
            ('Radiation oncology', 'Radiation oncology'),
            ('Surgery', 'Surgery'),
            ('Urology', 'Urology'),
        ])
    concern_description = TextAreaField('concern_description', validators=[DataRequired(), Length(max=500)])
    
###################################################################################################################

class DoctorForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'), ]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    facebook_link = StringField(
        'facebook_link', validators= [Optional(), URL()]
    )
    twiter_link = StringField(
        'twiter_link', validators= [Optional(), URL()]
    )
    linkedin_link = StringField(
        'linkedin_link', validators= [Optional(), URL()]
    )
    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
    )
    
    specialities = SelectField(
        'specialities', validators=[DataRequired()],
        choices=[
            ('Allergy and immunology', 'Allergy and immunology'),
            ('Dermatology', 'Dermatology'),
            ('Diagnostic radiology', 'Diagnostic radiology'),
            ('Emergency medicine', 'Emergency medicine'),
            ('Family medicine', 'Family medicine'),
            ('Internal medicine', 'Internal medicine'),
            ('Medical genetics', 'Medical genetics'),
            ('Neurology', 'Neurology'),
            ('Nuclear medicine', 'Nuclear medicine'),
            ('Obstetrics and gynecology', 'Obstetrics and gynecology'),
            ('Ophthalmology', 'Ophthalmology'),
            ('Pathology', 'Pathology'),
            ('Pediatrics', 'Pediatrics'),
            ('Physical medicine and rehabilitation', 'Physical medicine and rehabilitation'),
            ('Preventive medicine', 'Preventive medicine'),
            ('Psychiatry', 'Psychiatry'),
            ('Radiation oncology', 'Radiation oncology'),
            ('Surgery', 'Surgery'),
            ('Urology', 'Urology'),
        ])