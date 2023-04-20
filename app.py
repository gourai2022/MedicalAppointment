#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from ast import parse
from operator import itemgetter
import re
from sqlalchemy.exc import SQLAlchemyError
#from distutils.command.sdist import appointment_formats
import sys
import json
import dateutil.parser
import babel
from flask import Flask, abort, render_template, request, Response, flash, redirect, url_for, abort, jsonify, session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from sqlalchemy import func, true
from flask_migrate import Migrate
from datetime import datetime, date
from flask_wtf.csrf import CSRFProtect
from dateutil import parser
from models import *
from forms import *
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

#----------------------------------------------------------------------------#
# Home Page.
#----------------------------------------------------------------------------#
    @app.route('/')
    def index():
      return render_template('/pages/home.html/')

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

    def calculate_age(born):
        today = date.today()
        try: 
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month+1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

  #########################################DONE##########################################################################


  #----------------------------------------------------------------------------#
  # Controllers.
  #----------------------------------------------------------------------------#

    todat_date = date.today().strftime('%Y-%m-%d')
  #  doctors
  #  ----------------------------------------------------------------

    @app.route("/doctors")
    def doctors():
      form = DoctorForm()
      doctors = Doctor.query.with_entities(Doctor.id, Doctor.name).all()
      return render_template('pages/doctors.html', form=form, doctors=doctors)

  #########################################DONE##########################################################################

    @app.route('/doctors/<int:doctor_id>')
    def doctor_details(doctor_id):
      form = DoctorForm()
      past_appointment_query = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.appo_day < todat_date).order_by(Appointment.appo_day).all()
      upcoming_appointment_query = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.appo_day > todat_date).order_by(Appointment.appo_day).all()
      doctor = Doctor.query.get(doctor_id)
      past_appointments = []
      upcoming_appointments = []
      try:
        data={
          "id": doctor_id,
          "name": doctor.name,
          "gender": doctor.gender,
          "address": doctor.address,
          "city": doctor.city,
          "state": doctor.state,
          "phone": doctor.phone,
          #"appo_location": doctor.appo_location,
          "facebook_link": doctor.facebook_link,
          "twiter_link": doctor.twiter_link,
          "linkedin_link": doctor.linkedin_link,
          "website_link": doctor.website_link,
          "specialities": doctor.specialities,
          #"past_appointments": past_appointments,
          #"upcoming_appointments": upcoming_appointments,
          "past_appo": len(past_appointment_query),
          "upcoming_appo": len(upcoming_appointment_query)
        }
        return render_template('pages/doctor_details.html', doctor=data)
      
      except SQLAlchemyError as e:
          #error = str(e.__dict__['orig'])
          #flash( error)
          print(f'Exception "{e}" in create_doctor_submission()')
          flash('An error occurred')
          db.session.rollback()
      finally:
          db.session.close()    
      
  #########################################DONE##########################################################################  

  #  Create doctor
  #  ----------------------------------------------------------------

    @app.route('/doctors/create', methods=['GET'])
    def create_doctor_form():
      form = DoctorForm()
      return render_template('forms/new_doctor.html', form=form)

    @app.route('/doctors/create', methods=['POST'])
    def create_doctor_submission():
      form = DoctorForm()
      new_doctor = Doctor()
      new_doctor.name = request.form.get('name').strip()
      new_doctor.address =request.form.get('address')
      new_doctor.gender = request.form.get('gender')
      new_doctor.city = request.form.get('city')
      new_doctor.state =request.form.get('state')
      phone =request.form.get('phone')
      new_doctor.phone = re.sub('\D', '', phone) 
      new_doctor.facebook_link =request.form.get('facebook_link').strip()
      new_doctor.twiter_link =request.form.get('twiter_link').strip()
      new_doctor.linkedin_link =request.form.get('linkedin_link').strip()
      new_doctor.website_link =request.form.get('website_link').strip()
      ##new_doctor.specialities = True if request.form.get('seeking_talent') == 'y' else False
      new_doctor.specialities = request.form.get('specialities') 
      new_doctor.upcoming_appo = 0
      new_doctor.past_appo = 0
      
      # Redirect back to form if errors in form validation
      if not form.validate():
        flash( form.errors )
        flash('An error occurred. name ' + new_doctor.name + ' could not be validate.')
        return render_template('pages/home.html')
      else:
        try:
          db.session.add(new_doctor)
          db.session.commit()
          flash('doctor ' + new_doctor.name + ' was successfully listed!')
          return render_template('pages/home.html')
        except SQLAlchemyError as e:
          error = str(e.__dict__['orig'])
          flash( error)
          print(f'Exception "{e}" in create_doctor_submission()')
          flash('An error occurred. doctor ' + new_doctor.name + ' could not be listed.')
          db.session.rollback()
        finally:
          db.session.close()
          return render_template('pages/home.html')    
      
  #########################################DONE##########################################################################

    @app.route('/doctors/<int:doctor_id>/edit', methods=['GET'])
    def edit_doctor(doctor_id):
      form = DoctorForm()
      doctor_edit = Doctor.query.get(doctor_id)
      if doctor_edit: 
        form.name.data = doctor_edit.name
        form.gender.data = doctor_edit.gender
        form.address.data = doctor_edit.address
        form.city.data = doctor_edit.city
        form.state.data = doctor_edit.state
        form.phone.data = doctor_edit.phone
        form.facebook_link.data = doctor_edit.facebook_link
        form.twiter_link.data = doctor_edit.twiter_link
        form.linkedin_link.data = doctor_edit.linkedin_link
        form.website_link.data = doctor_edit.website_link
        form.specialities.data = doctor_edit.specialities
        
      return render_template('forms/edit_doctor.html', form=form, doctor=doctor_edit)

  #########################################DONE##########################################################################

    @app.route('/doctors/<int:doctor_id>/edit', methods=['POST'])
    def edit_doctor_submission(doctor_id):
      #error = False 
      form = DoctorForm() 
      update_doctor = Doctor.query.get(doctor_id)
      update_doctor.name = request.form.get('name').strip()
      update_doctor.gender =  request.form.get('gender')
      update_doctor.address =  request.form.get('address')
      update_doctor.city = request.form.get('city')
      update_doctor.state =  request.form.get('state')
      update_doctor.phone =  request.form.get('phone')
      update_doctor.facebook_link =  request.form.get('facebook_link').strip()
      update_doctor.twiter_link =  request.form.get('twiter_link').strip()
      update_doctor.linkedin_link =  request.form.get('linkedin_link').strip()
      update_doctor.website_link =  request.form.get('website_link').strip()
      ##update_doctor.seeking_talent =  True if request.form.get('seeking_talent') == 'y' else False
      update_doctor.specialities =  request.form.get('specialities')
      
      if not form.validate():
        flash( form.errors )
        flash('An error occurred. doctor could not be validate.')
        return render_template('pages/home.html')
      else:
        try:
          #db.session.execute(update_doctor)
          db.session.merge(update_doctor)
          db.session.commit()
          flash('doctor ' + update_doctor.name + ' successfully Updated')  
          return render_template('pages/home.html')
        except SQLAlchemyError as e:
          error = str(e.__dict__['orig'])
          flash( error)
          print(f'Exception "{e}" in create_doctor_submission()')
          db.session.rollback()
          flash('An error occurred. doctor ' + update_doctor.name + ' could not be listed.')
        finally:
          db.session.close()  
          return render_template('pages/home.html')     
          
  #########################################DONE##########################################################################
    
    @app.route('/doctors/delete/<int:id>')
    def delete_doctor(id):
        delete_doctor = Doctor.query.filter_by(id=id).first()
        flash('Doctor "' + delete_doctor.name + '" can not be deleted due to user restictions.')
        return render_template('pages/home.html')
    '''    
        try:
          db.session.delete(delete_doctor)
          db.session.commit()
          #doctors = Doctor.query.all()
          flash("Docor Was Deleted!")
          return render_template('pages/home.html')
        except SQLAlchemyError as e:
          flash(sys.exc_info())
          db.session.rollback()
          flash('please try again. doctor could not be deleted.')
          return render_template('pages/home.html')
        finally:
          db.session.close()    
          return render_template('pages/home.html')
    '''    
  #########################################DONE##########################################################################
  #  patients
  #  ----------------------------------------------------------------
    @app.route('/patients')
    def patients():
      form = DoctorForm()
      #patient_seeking_specialities = Patient.query.filter_by(Patient.seeking_specialities).all()
      #patient_health_insurance_provider = Patient.query.filter_by(Patient.health_insurance_provider).all()
      patients = Patient.query.with_entities(Patient.id, Patient.name).all()
      return render_template('pages/patients.html', patients=patients)
  #########################################DONE########################################################################## 

    @app.route('/patients/<int:patient_id>')
    def patient_details(patient_id):
      past_appointment_query = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.appo_day < todat_date).order_by(Appointment.appo_day).all()
      upcoming_appointment_query = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.appo_day > todat_date).order_by(Appointment.appo_day).all()
      patient = Patient.query.get(patient_id)
      #appointments = patient.appointments
      ##upcoming_appointments = []
      try:
        
        data = {
          "id": patient_id,
          "name": patient.name,
          "gender": patient.gender, 
          "address": patient.address,
          "city": patient.city,
          "state": patient.state,
          "phone": patient.phone,
          "date_of_birth": patient.date_of_birth,
          "health_insurance_provider":patient.health_insurance_provider,
          "health_insurance_id": patient.health_insurance_id,
          "seeking_specialities": patient.seeking_specialities,
          "concern_description":patient.concern_description,
          "past_appo": len(past_appointment_query),
          "upcoming_appo": len(upcoming_appointment_query)
        }
        return render_template('pages/patient_details.html', patient=data)   
      except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash( error)
        print(f'Exception "{e}" in create_doctor_submission()')
        flash('An error occurred')
        db.session.rollback()
      finally:
        db.session.close()
      
  #########################################DONE##########################################################################
  #  delete patient
  #  ----------------------------------------------------------------
    
    @app.route('/patients/delete/<int:id>')
    def delete_patient(id):
      deleted_patient = Patient.query.filter_by(id=id).first()
      flash('Patient "' + deleted_patient.name + '" can not be deleted due to user restictions.')
      return render_template('pages/home.html')
      '''
      try:
        db.session.delete(deleted_patient)
        #db.session.remove(deleted_patient)
        db.session.commit()
        flash('patient ' + deleted_patient.name + ' was successfully deleted!')
        return render_template('pages/home.html')
      except:
        db.session.rollback()
        flash('please try again. doctor ' + deleted_patient.id + ' could not be deleted.')
      finally:
        db.session.close()
        return render_template('pages/home.html')
      '''
    #########################################DONE##########################################################################
  #  Update
  #  ----------------------------------------------------------------

    @app.route('/patients/<int:patient_id>/edit', methods=['GET'])
    def edit_patient(patient_id):
      form = PatientForm()
      patient_edit = Patient.query.get(patient_id)
      if patient_edit: 
        form.name.data = patient_edit.name
        form.gender.data = patient_edit.gender
        form.address.data = patient_edit.address
        form.city.data = patient_edit.city
        form.state.data = patient_edit.state
        form.phone.data = patient_edit.phone
        date_string = patient_edit.date_of_birth
        form.date_of_birth.data = datetime.strptime(date_string, '%Y-%m-%d')
        #form.date_of_birth.data = patient_edit.date_of_birth.strptime('%d/%m/%Y')
        form.health_insurance_provider.data = patient_edit.health_insurance_provider
        form.health_insurance_id.data = patient_edit.health_insurance_id
        form.seeking_specialities.data = patient_edit.seeking_specialities
        form.concern_description.data = patient_edit.concern_description
      return render_template('forms/edit_patient.html', form=form, patient=patient_edit)
  #########################################DONE##########################################################################

    @app.route('/patients/<int:patient_id>/edit', methods=['POST'])
    def edit_patient_submission(patient_id):
      form = PatientForm()
      #update_patient = patient.query.filter(patient.id == patient_id)
      update_patient = Patient.query.get(patient_id)
      update_patient.name = request.form.get('name').strip()
      update_patient.gender = request.form.get('gender')
      update_patient.address = request.form.get('address')
      update_patient.city = request.form.get('city')
      update_patient.state =  request.form.get('state')
      update_patient.phone =  request.form.get('phone')
      update_patient.date_of_birth =  str(request.form.get('date_of_birth'))
      update_patient.health_insurance_provider =  request.form.get('health_insurance_provider').strip()
      update_patient.health_insurance_id =  request.form.get('health_insurance_id')
      update_patient.seeking_specialities =  request.form.get('seeking_specialities')
      update_patient.concern_description =  request.form.get('concern_description')
      #update_patient.concern_description =  request.form.get('concern_description')
      if not form.validate():
        flash( form.errors )
        flash('An error occurred. patient could not be validate.')
        return render_template('pages/home.html')
      else:
        try:
          db.session.merge(update_patient)
          db.session.commit()
          flash('patient ' + update_patient.name + ' successfully Updated')  
          #return redirect(url_for('appointment_patient', patient_id=patient_id))
          return render_template('pages/home.html')
        except SQLAlchemyError as e:
          error = str(e.__dict__['orig'])
          flash( error)
          print(f'Exception "{e}" in edit_patient_submission()')
          db.session.rollback()
          flash('An error occurred. patient ' + update_patient.name + ' could not be listed.')
        finally:
          db.session.close()       
          return render_template('pages/home.html')

  #########################################DONE##########################################################################  

  #  Create patient
  #  ----------------------------------------------------------------

    @app.route('/patients/create', methods=['GET'])
    def create_patient_form():
      form = PatientForm()
      return render_template('forms/new_patient.html', form=form)

  #########################################DONE##########################################################################  

    @app.route('/patients/create', methods=['POST'])
    def create_patient_submission():
      form = PatientForm()
      new_patient = Patient()
      new_patient.name = request.form.get('name').strip()
      new_patient.gender = request.form.get('gender')
      new_patient.address = request.form.get('address')
      new_patient.city = request.form.get('city')
      new_patient.state = request.form.get('state')
      phone = request.form.get('phone')
      new_patient.phone = re.sub('\D', '', phone) 
      new_patient.date_of_birth = request.form.get('date_of_birth')
      new_patient.health_insurance_provider =request.form.get('health_insurance_provider').strip()
      new_patient.health_insurance_id =request.form.get('health_insurance_id')
      new_patient.seeking_specialities = request.form.get('seeking_specialities')
      new_patient.concern_description = request.form.get('concern_description') 
      new_patient.upcoming_appo = 0
      new_patient.past_appo = 0
      
      # Redirect back to form if errors in form validation
      if not form.validate():
        flash( form.errors )
        flash('An error occurred. name ' + new_patient.name + ' could not be validate.')
        return render_template('pages/home.html')
      else:
        try:
          db.session.add(new_patient)
          db.session.commit()
          flash('patient ' + new_patient.name + ' was successfully listed!')
          return render_template('pages/home.html')
        except SQLAlchemyError as e:
          error = str(e.__dict__['orig'])
          flash( error)
          print(f'Exception "{e}" in create_doctor_submission()')
          flash('An error occurred. patient ' + new_patient.name + ' could not be listed.')
          db.session.rollback()
        finally:
          db.session.close()
        return render_template('pages/home.html')

  #########################################DONE##########################################################################
  #  appointments
  #  ----------------------------------------------------------------

    @app.route("/appointments", methods=["POST","GET"])
    def appointments():
      form = AppointmentForm()
      data = []
      upcoming_appointments = Appointment.query.order_by(Appointment.appo_day).all()
      #appointments = Appointment.query.all()
      try:  
        if upcoming_appointments != None:
          for appointment in upcoming_appointments:
            data.append({
            "doctor_id": appointment.doctor_id,
            "doctor_name": Doctor.query.get(appointment.doctor_id).name,
            "patient_id": appointment.patient_id,
            "patient_name": Patient.query.get(appointment.patient_id).name,
            "appo_day": appointment.appo_day,
            "appo_time": appointment.appo_time
            })
      except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash( error)
        print(f'Exception "{e}" in appointments()')
        flash('An error occurred. Appointment is not listed.')
      
      return render_template('pages/appointments.html',form=form, appointments=upcoming_appointments)
  #########################################DONE##########################################################################

    @app.route('/appointments/create')
    def create_appointments():
      # renders form. do not touch.
      form = AppointmentForm()
      return render_template('forms/new_appointment.html', form=form)
  #########################################DONE##########################################################################
    
    @app.route('/appointments/create', methods=['POST'])
    def create_appointment_submission():
      form = AppointmentForm()
      new_appointment = Appointment()
      new_appointment.patient_id = request.form.get('patient_id')
      new_appointment.doctor_id = request.form.get('doctor_id')
      new_appointment.appo_day = request.form.get('appo_day')
      new_appointment.appo_time = request.form.get('appo_time')
      appointment_time = new_appointment.appo_time
      # Redirect back to form if errors in form validation
      if not form.validate():
        flash( form.errors )
        flash('An error occurred. appointment could not be validate.')
        return render_template('pages/home.html')
      else:
        try:
          db.session.add(new_appointment)
          #db.session.commit()
          
          updated_patient = Patient.query.get(new_appointment.patient_id)
          updated_doctor = Doctor.query.get(new_appointment.doctor_id)

          if appointment_time < date.today().strftime('%Y-%m-%d'):
            updated_patient.upcoming_appo = int(updated_patient.upcoming_appo + 1) 
            updated_doctor.upcoming_appo = int(updated_doctor.upcoming_appo + 1)
    
          elif appointment_time > date.today().strftime('%Y-%m-%d'):
            updated_patient.past_appo = int(updated_patient.past_appo + 1)
            updated_doctor.past_appo = int(updated_doctor.past_appo + 1)
          
          db.session.merge(updated_patient)
          db.session.merge(updated_doctor)
          
          db.session.commit()
          #flash('upcoming appointment patient -' + str(updated_patient.upcoming_appo) + 'and doctor-' + str(updated_doctor.upcoming_appo))
          #flash('Past appointment patient -' + str(updated_doctor.past_appo) + 'and doctor-' + str(updated_doctor.past_appo))
          flash('New appointment was successfully listed!')
          return render_template('pages/home.html')
        except SQLAlchemyError as e:
          error = str(e.__dict__['orig'])
          flash( error)
          flash('An error occurred. appointment could not be listed.')
          db.session.rollback()
        finally:
          db.session.close()
          return render_template('pages/home.html')

  #########################################DONE##########################################################################
    @app.route('/appointments/<int:appointment_id>/edit', methods=['GET'])
    def edit_appointment(appointment_id):
      form = AppointmentForm()
      appointment_edit = Appointment.query.get(appointment_id)
      if appointment_edit: 
        app_date_string = appointment_edit.appo_day
        form.appo_day.data = datetime.strptime(app_date_string, '%Y-%m-%d')
        form.appo_time.data = appointment_edit.appo_time
        #form.appo_available.data = appointment_edit.appo_available
      return render_template('forms/edit_appointment.html', form=form, appointment=appointment_edit)
  #########################################DONE##########################################################################

    @app.route('/appointments/<int:appointment_id>/edit', methods=['POST'])
    def edit_appointment_submission(appointment_id):
      form = AppointmentForm()
      update_appointment = Appointment.query.get(appointment_id)
      
      update_appointment.appo_day =  str(request.form.get('appo_day'))
      update_appointment.appo_time = request.form.get('appo_time')
      #update_appointment.appo_available = False if request.form.get('checked') else True
      
      try:
        db.session.merge(update_appointment)
        db.session.commit()

        flash('Appointment ' + str(update_appointment.id) + ' successfully Updated') 
        return render_template('pages/home.html')   
      except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash( error)
        print(f'Exception "{e}" in edit_appointment_submission()')
        flash('An error occurred')
        db.session.rollback()
      finally:
        db.session.close()
  #########################################DONE##########################################################################
    @app.route('/appointments/<int:appointment_id>')
    def appointment_details(appointment_id):
      appointment = Appointment.query.get(appointment_id)
      try:
        data = ({
          "id": appointment_id,
          "doctor_id": appointment.doctor_id,
          "patient_id": appointment.patient_id,
          "appo_day": appointment.appo_day,
          "appo_time": appointment.appo_time
        })
        
        #doctor = Doctor.query.filter(Doctor.id == appointment.doctor_id).name
        doctor = Doctor.query.filter(Doctor.id == appointment.doctor_id).first()
        doctor_name = doctor.name
        
        patient = Patient.query.filter(Patient.id == appointment.patient_id).first()
        patient_name = patient.name
        
        
        return render_template('pages/appointment_details.html', appointment=data, doctor=doctor_name, patient=patient_name)   
      except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash( error)
        print(f'Exception "{e}" in appointment_details()')
        flash('An error occurred')
        db.session.rollback()
      finally:
        db.session.close()
  #########################################DONE##########################################################################
    
    @app.route('/appointments/delete/<int:id>')
    def delete_appointment(id):
        form = DoctorForm()
        delete_appointment = Appointment.query.filter_by(id=id).first()

        updated_patient = Patient.query.get(delete_appointment.patient_id)
        updated_doctor = Doctor.query.get(delete_appointment.doctor_id)

        if delete_appointment != None :
          if delete_appointment.appo_day < date.today().strftime("%Y/%m/%d"):
            updated_patient.upcoming_appo = int(updated_patient.upcoming_appo - 1) 
            updated_doctor.upcoming_appo = int(updated_doctor.upcoming_appo - 1)

          #elif new_appointment.appo_day.strptime() < parse(date.today().strftime("%y/%m/%")): 
          elif delete_appointment.appo_day > date.today().strftime("%Y/%m/%d"):
            updated_patient.past_appo = int(updated_patient.past_appo - 1)
            updated_doctor.past_appo = int(updated_doctor.past_appo - 1)
        try:
          #session.clear()
          #session.refresh()
          db.session.delete(delete_appointment)
          db.session.merge(updated_patient)
          db.session.merge(updated_doctor)
          db.session.commit()
          flash("Appointment is Deleted!")
          return render_template("pages/home.html")
        except SQLAlchemyError as e:
          flash(sys.exc_info())
          db.session.rollback()
          flash('please try again. Appointment could not be deleted.')
          return render_template("pages/home.html")
        finally:
          db.session.close()
    
  #########################################DONE##########################################################################

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}), 
            400,
        )

    @app.errorhandler(404)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Page not found"}), 
            404,
        )

    @app.errorhandler(405)
    def invalid_method(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Invalid method"}), 
            405,
        )

    @app.errorhandler(422)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable recource"}), 
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal server error"}), 
            500,
        )    

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
  

app = create_app()

if __name__ == '__main__':
    app.run()