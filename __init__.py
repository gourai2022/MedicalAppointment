import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from datetime import date, datetime
from models import setup_db, Appointment, Doctor, Patient

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    todat_date = date.today().strftime('%Y-%m-%d')
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
            )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
            )
        return response
    
    ## GET DATA #############################################################################################
    
    @app.route("/doctors")
    @requires_auth("get:doctors")
    def doctors(payload):
      doctors = Doctor.query.all()
      for doctor in doctors:
            return jsonify({
                        "id" : doctor.id,
                        "name": doctor.name,
                    })
      
    @app.route("/patients")
    @requires_auth("get:patients")
    def patients(payload):
      patients = Patient.query.all()
      for patient in patients:
            return jsonify({
                        "id" : patient.id,
                        "name": patient.name,
                    })
      
    @app.route("/appointments")
    @requires_auth("get:appointments")
    def appointments(payload):
      appointments = Appointment.query.all()
      for appointment in appointments:
            return jsonify({
                        "id" : appointment.id,
                        "appo_day": appointment.appo_day,
                        "appo_time": appointment.appo_time,
                    })    
      
    ## RECORD DETAILS #############################################################################################  

    @app.route('/doctors/<int:doctor_id>')
    @requires_auth("get:doctor_details")
    def doctor_details(payload, doctor_id):
        try:
            past_appointment_query = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.appo_day < todat_date).order_by(Appointment.appo_day).all()
            upcoming_appointment_query = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.appo_day > todat_date).order_by(Appointment.appo_day).all()
            doctor = Doctor.query.get(Doctor.id == doctor_id)
            if doctor != None:
                return jsonify({
                            "id": doctor_id,
                            "name": doctor.name,
                            "gender": doctor.gender,
                            "address": doctor.address,
                            "city": doctor.city,
                            "state": doctor.state,
                            "phone": doctor.phone,
                            "facebook_link": doctor.facebook_link,
                            "twiter_link": doctor.twiter_link,
                            "linkedin_link": doctor.linkedin_link,
                            "website_link": doctor.website_link,
                            "specialities": doctor.specialities,
                            "past_appo": len(past_appointment_query),
                            "upcoming_appo": len(upcoming_appointment_query)
                        })
        except Exception as e:
            print(f'Exception "{e}" in doctor_details()')
            abort(400)      
        
    @app.route('/patients/<int:patient_id>')
    @requires_auth("get:patient_details")
    def patient_details(payload, patient_id):
        try:
            past_appointment_query = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.appo_day < todat_date).order_by(Appointment.appo_day).all()
            upcoming_appointment_query = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.appo_day > todat_date).order_by(Appointment.appo_day).all()
            patient = Patient.query.get(Patient.id == patient_id)
            if patient != None:
                return jsonify({
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
                        })
        except Exception as e:
            print(f'Exception "{e}" in patient_details()')
            abort(400)    

    @app.route('/appointments/<int:appointment_id>')
    @requires_auth("get:appointment_details")
    def appointment_details(payload, appointment_id):
        try:
            appointment = Appointment.query.get(Appointment.id == appointment_id)    
            if appointment != None:
                return jsonify({
                            "id": appointment_id,
                            "doctor_id": appointment.doctor_id,
                            "patient_id": appointment.patient_id,
                            "appo_day": appointment.appo_day,
                            "appo_time": appointment.appo_time
                        })
        except Exception as e:
            print(f'Exception "{e}" in appointment_details()')
            abort(400)    

    ## CREATE RECORD #############################################################################################  

    @app.route('/doctors/create', methods=['POST'])
    @requires_auth("post:create_doctor")
    def create_doctor(payload):    
        new_doctor = Doctor()
        body = request.get_json()

        new_doctor.name = body.get('name').strip()
        new_doctor.address =body.get('address')
        new_doctor.gender = body.get('gender')
        new_doctor.city = body.get('city')
        new_doctor.state = body.get('state')
        phone = body.get('phone')
        new_doctor.phone = re.sub('\D', '', phone) 
        new_doctor.facebook_link = body.get('facebook_link').strip()
        new_doctor.twiter_link = body.get('twiter_link').strip()
        new_doctor.linkedin_link = body.get('linkedin_link').strip()
        new_doctor.website_link = body.get('website_link').strip()
        new_doctor.specialities = body.get('specialities') 
        new_doctor.upcoming_appo = 0
        new_doctor.past_appo = 0

        try:
            new_doctor.insert()
            return jsonify({
                    "success": True,
                    "id": new_doctor.id,
                    "name": new_doctor.name,
            })
        except Exception as e:
            print(f'Exception "{e}" in create_doctor()')
            abort(422)

    @app.route('/patients/create', methods=['POST'])
    @requires_auth("post:create_patient")
    def create_patient(payload):    
        new_patient = Patient()
        body = request.get_json()
        new_patient = Patient()
        new_patient.name = body.get('name').strip()
        new_patient.gender = body.get('gender')
        new_patient.address = body.get('address')
        new_patient.city = body.get('city')
        new_patient.state = body.get('state')
        phone = body.get('phone')
        new_patient.phone = re.sub('\D', '', phone) 
        new_patient.date_of_birth = body.get('date_of_birth')
        new_patient.health_insurance_provider =body.get('health_insurance_provider').strip()
        new_patient.health_insurance_id =body.get('health_insurance_id')
        new_patient.seeking_specialities = body.get('seeking_specialities')
        new_patient.concern_description = body.get('concern_description') 
        new_patient.upcoming_appo = 0
        new_patient.past_appo = 0
        
        try:
            new_patient.insert()
            return jsonify({
                    "success": True,
                    "id": new_patient.id,
                    "name": new_patient.name,
            })
        except Exception as e:
            print(f'Exception "{e}" in create_patient()')
            abort(422)

    @app.route('/appointments/create', methods=['POST'])
    @requires_auth("post:create_appointment")
    def create_appointment(payload):
        new_appointment = Appointment()
        new_appointment.patient_id = request.json.get('patient_id')
        new_appointment.doctor_id = request.json.get('doctor_id')
        new_appointment.appo_day = request.json.get('appo_day')
        new_appointment.appo_time = request.json.get('appo_time')
        appointment_time = new_appointment.appo_time
        try:
            new_appointment.insert()
            updated_patient = Patient.query.get(new_appointment.patient_id)
            updated_doctor = Doctor.query.get(new_appointment.doctor_id)

            if appointment_time < date.today().strftime('%Y-%m-%d'):
                updated_patient.upcoming_appo = int(updated_patient.upcoming_appo + 1) 
                updated_doctor.upcoming_appo = int(updated_doctor.upcoming_appo + 1)
        
            elif appointment_time > date.today().strftime('%Y-%m-%d'):
                updated_patient.past_appo = int(updated_patient.past_appo + 1)
                updated_doctor.past_appo = int(updated_doctor.past_appo + 1)
          
            updated_patient.merge()
            updated_patient.merge()

            return jsonify({
                    "success": True,
                    "id": new_appointment.id,
                    "appo_day": new_appointment.appo_day,
            })
        except Exception as e:
            print(f'Exception "{e}" in create_appointment()')
            abort(422)

    ## UPDATE RECORD #############################################################################################  

    @app.route('/doctors/<int:doctor_id>/edit', methods=['POST'])
    @requires_auth("patch:edit_doctor")
    def edit_doctor(payload, doctor_id):   
        update_doctor = Doctor.query.get(Doctor.id == doctor_id)
        if update_doctor: 
            data = {
                "id": doctor_id,
                "name": update_doctor.name,
                "gender": update_doctor.gender,
                "address": update_doctor.address,
                "city": update_doctor.city,
                "state": update_doctor.state,
                "phone": update_doctor.phone,
                "facebook_link": update_doctor.facebook_link,
                "twiter_link": update_doctor.twiter_link,
                "linkedin_link": update_doctor.linkedin_link,
                "website_link": update_doctor.website_link,
                "specialities": update_doctor.specialities
                }
            
            update_doctor.name = request.json.get('name').strip()
            update_doctor.gender =  request.json.get('gender')
            update_doctor.address =  request.json.get('address')
            update_doctor.city = request.json.get('city')
            update_doctor.state =  request.json.get('state')
            update_doctor.phone =  request.json.get('phone')
            update_doctor.facebook_link =  request.json.get('facebook_link').strip()
            update_doctor.twiter_link =  request.json.get('twiter_link').strip()
            update_doctor.linkedin_link =  request.json.get('linkedin_link').strip()
            update_doctor.website_link =  request.json.get('website_link').strip()
            update_doctor.specialities =  request.json.get('specialities')

            update_doctor.update()

            return jsonify({
                "success": True,
                "updated": update_doctor.format()
            })
       
    
    @app.route('/patient/<int:patient_id>/edit', methods=['POST'])
    @requires_auth("patch:edit_patient")
    def edit_patient(payload, patient_id):
        update_patient = Patient.query.get(Patient.id == patient_id)
        if update_patient: 
            data = {
                "id": patient_id,
                "name": update_patient.name,
                "gender": update_patient.gender,
                "address": update_patient.address,
                "city": update_patient.city,
                "state": update_patient.state,
                "phone": update_patient.phone,
                "facebook_link": update_patient.facebook_link,
                "twiter_link": update_patient.twiter_link,
                "linkedin_link": update_patient.linkedin_link,
                "website_link": update_patient.website_link,
                "specialities": update_patient.specialities
                }
           
            update_patient.name = request.json.get('name').strip()
            update_patient.gender = request.json.get('gender')
            update_patient.address = request.json.get('address')
            update_patient.city = request.json.get('city')
            update_patient.state =  request.json.get('state')
            update_patient.phone =  request.json.get('phone')
            update_patient.date_of_birth =  str(request.json.get('date_of_birth'))
            update_patient.health_insurance_provider =  request.json.get('health_insurance_provider').strip()
            update_patient.health_insurance_id =  request.json.get('health_insurance_id')
            update_patient.seeking_specialities =  request.json.get('seeking_specialities')
            update_patient.concern_description =  request.json.get('concern_description')
            
            update_patient.update()

            return jsonify({
                "success": True,
                "updated": update_patient.format()
            })
        
    @app.route('/appointments/<int:appointment_id>/edit', methods=['POST'])
    @requires_auth("patch:edit_appointment")
    def edit_appointment(payload, appointment_id):
        update_appointment = Appointment.query.get(Appointment.id == appointment_id)
        if update_appointment: 
            data = {
                "id": appointment_id,
                "doctor_id": update_appointment.doctor_id,
                "patient_id": update_appointment.patient_id,
                "appo_day": update_appointment.appo_day,
                "appo_time": update_appointment.appo_time }

        update_appointment.appo_day =  str(request.json.get('appo_day'))
        update_appointment.appo_time = request.json.get('appo_time')
        
        update_appointment.update()

        return jsonify({
                "success": True,
                "updated": update_appointment.format()
            })
    
    ## DELETE RECORD #############################################################################################  
    
    @app.route('/appointments/delete/<int:id>')
    @requires_auth("delete:appointment")
    def delete_appointment(payload, id):
        delete_appointment = Appointment.query.filter_by(id=id).first()
        updated_patient = Patient.query.get(delete_appointment.patient_id)
        updated_doctor = Doctor.query.get(delete_appointment.doctor_id)
        if delete_appointment != None :
            if delete_appointment.appo_day < date.today().strftime("%Y/%m/%d"):
                updated_patient.upcoming_appo = int(updated_patient.upcoming_appo - 1) 
                updated_doctor.upcoming_appo = int(updated_doctor.upcoming_appo - 1)

            elif delete_appointment.appo_day > date.today().strftime("%Y/%m/%d"):
                updated_patient.past_appo = int(updated_patient.past_appo - 1)
                updated_doctor.past_appo = int(updated_doctor.past_appo - 1)

        delete_appointment.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })
    
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
    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({"success": False, "error": auth_error.status_code, "message": auth_error.error['description']}), auth_error.status_code  

    return app
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

app = create_app()

if __name__ == '__main__':
    app.run()