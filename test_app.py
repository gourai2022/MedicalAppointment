import os
import unittest
import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Appointment, Doctor, Patient
from forms import *

##########This class represents the Medapp test case##########
class MedappTestCase(unittest.TestCase):

###########Define test variables and initialize app.################
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "medapp"
        #self.database_path = "postgresql://{}/{}".format('gourikulkarni', 'Kumar18!', 'localhost:5432', self.database_name)
        #setup_db(self.app, self.database_path)

        #Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Set up authentication tokens info
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        admin_jwt = self.auth["roles"]["admin"]["jwt_token"]
        doctor_jwt = self.auth["roles"]["doctor"]["jwt_token"]
        patient_jwt = self.auth["roles"]["patient"]["jwt_token"]
        self.auth_headers = {
            "admin": f'Bearer {admin_jwt}',
            "doctor": f'Bearer {doctor_jwt}',
            "patient": f'Bearer {patient_jwt}'
        }   
    
##########Executed after reach test#######    
    def tearDown(self):
        pass

###########Tests for doctors successful operation and for expected errors.
  
    def test_get_doctors(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/doctors', headers=headers)
        response = self.app.get('/doctors', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['doctors']), type([]))
        self.assertTrue(response.is_json())
        self.assertTrue(len(response.get_json()) > 0)

    def test_create_doctor_success(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/doctors', headers=headers)
        response = self.app.get('/doctors/create', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['doctors']), type([]))
        
    def test_create_doctor_error(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/doctors', headers=headers)
        response = self.app.get('/doctors/create', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_get_doctor_edit_page_success(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            doctor_id = 2
            doctor_name = "Andy"
            response = request.patch(f'/doctors/{doctor_id}/edit', json={'name': doctor_name}, headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        #self.assertTrue(data['success'])
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['doctors']), type([]))
        self.assertEqual(data['updated']['title'], doctor_name)
    
    def test_get_doctor_edit_page_error(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            doctor_id = 99999
            doctor_name = "Andy Andy"
            response = request.patch(f'/doctors/{doctor_id}/edit', json={'name': doctor_name}, headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")

    def test_to_delete_doctor(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            doctor_id = 11
            response = request.patch(f'/doctors/{doctor_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_doctor_not_found_to_delete(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            doctor_id = 111111111
            response = request.patch(f'/doctors/{doctor_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")


###########Tests for patient successful operation and for expected errors.
  
    def test_get_patients(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/patients', headers=headers)
        response = self.app.get('/patients', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['patients']), type([]))
        self.assertTrue(response.is_json())
        self.assertTrue(len(response.get_json()) > 0)
        
    def test_create_patient_success(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/patients', headers=headers)
        response = self.app.get('/patients/create', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['patients']), type([]))
        
    def test_create_patient_error(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/patients', headers=headers)
        response = self.app.get('/patients/create', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")
        
    def test_get_patient_edit_page_success(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            patient_id = 2
            patient_name = "Andy"
            response = request.patch(f'/patients/{patient_id}/edit', json={'name': patient_name}, headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['patients']), type([]))
        self.assertEqual(data['updated']['title'], patient_name)    
    
    def test_get_patient_edit_page_error(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            patient_id = 1111111111
            patient_name = "Andy Andy"
            response = request.patch(f'/patients/{patient_id}/edit', json={'name': patient_name}, headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")        

    def test_to_delete_patient(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            patient_id = 11
            response = request.patch(f'/patients/{patient_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)        

    def test_patient_not_found_to_delete(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            patient_id = 111111111
            response = request.patch(f'/patients/{patient_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")


###########Tests for appointment successful operation and for expected errors.
  
    def test_get_appointments(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/appointments', headers=headers)
        response = self.app.get('/appointments', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['appointments']), type([]))
        self.assertTrue(response.is_json())
        self.assertTrue(len(response.get_json()) > 0)
        
    def test_create_appointment_success(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/appointments', headers=headers)
        response = self.app.get('/appointments/create', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['appointments']), type([]))
        
    def test_create_appointment_error(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            response = request.get(f'{self.base_url}/appointments', headers=headers)
        response = self.app.get('/appointments/create', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_get_appointment_edit_page_success(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            appointment_id = 2
            appointment_day = "2023-05-15"
            response = request.patch(f'/appointments/{appointment_id}/edit', json={'appo_day': appointment_day}, headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['appointments']), type([]))
        self.assertEqual(data['updated']['title'], appointment_day)        
    
    def test_get_appointment_edit_page_error(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            appointment_id = 1111111111
            appointment_day = "2099-05-15"
            response = request.patch(f'/doctors/{appointment_id}/edit', json={'appo_day': appointment_day}, headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")
        
    def test_to_delete_appointment(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            appointment_id = 11
            response = request.patch(f'/appointments/{appointment_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)   

    def test_appointment_not_found_to_delete(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            appointment_id = 111111111
            response = request.patch(f'/appointments/{appointment_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()