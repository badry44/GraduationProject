# -*- coding: utf-8 -*-
import flask
from classes.Patient import Patient
from classes.DBHandler import DB

from flaskext.mysql import MySQL


class PController:

    def __init__(self, app):
        self.app = app

    def addPatientt(self, p):
        db = DB(self.app)
        insertUserCommand = ("INSERT INTO profile (username, password,first_name, last_name,age,email,phone) VALUES(%s, %s ,%s, %s, %s, %s, %s)")
        insertUserValues = (str(p.getUsername()), str(p.getPassword()), str(p.getFirstname()), str(
            p.getLastname()), p.getAge(), str(p.getEmail()), str(p.getPhone()))
        db.executeCommandWithoutResult(insertUserCommand, insertUserValues)

    def getPatientts(self):
        db = DB(self.app)
        patients = db.executeCommandWithResult("SELECT * FROM profile")
        return patients

    def getPatientByUserName(self, usernamee):
        db = DB(self.app)
        patients = db.executeCommandWithResult(
            "SELECT * FROM profile WHERE username='"+usernamee+"'")
        return patients

    def getPatientByID(self, idd):
        db = DB(self.app)
        patients = db.executeCommandWithResult("SELECT * FROM profile WHERE user_id='"+idd+"'")
        return patients
    
    def getPatientByUserNamepassword(self,usernamee,password):
        db = DB(self.app)
        patients = db.executeCommandWithResult(
            "SELECT * FROM profile WHERE username='"+usernamee+"' and password='"+password+"'")
        return patients
    def updatePatientByFieldAndCondition(self,feild,condtion):
        db = DB(self.app)
        patients = db.executeCommandWithoutResult("update profile set "+feild +" = where "+condtion)
        return patients

