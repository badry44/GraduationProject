import flask
import sys
from flask import request, jsonify, render_template, flash, redirect, url_for, session, logging
from flask import abort
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import logging
import os
import requests
from classes.Patient import Patient
from classes.DBHandler import DB
from classes.PatientController import PController
import classes.configrations as config
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
config.configApp(app)
logging.basicConfig(filename='app.log', format='%(asctime)s : -%(message)s', filemode='w')
PatientController = PController(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html')


@app.route('/uploadimage', methods=['GET', 'POST'])
def getImageAndRunScript():
    try:
        serverImageUrl = ''
        if request.method == 'POST':
            uploadedImage = request.files['pic']
            uploadedImageName = secure_filename(uploadedImage.filename)
            uploadedImage.save(os.path.join(app.config['UPLOAD_FOLDER'], uploadedImageName))
            serverImageUrl = os.path.join(app.config['UPLOAD_FOLDER'], uploadedImageName)
        else:
            return jsonify({"error": "This is not a Post Method Please make a Post with image with name (pic)",
                            "class": "None",
                            "accuracy": "None"
                            })

        modelUrl = os.getcwd() + "\\other\\trainedModel.model"
        labelUrl = os.getcwd() + "\\other\\labels.pickle"
        from other import Prediction as importedScript
        classResult, accuracyResult = importedScript.predict(serverImageUrl, modelUrl, labelUrl)
        return jsonify({"error": "Nothing",
                        "class": str(classResult),
                        "accuracy": str(accuracyResult)
                        })
    except Exception as e:
        logging.exception(str(e))
        return jsonify({"error": str(e),
                        "class": "None",
                        "accuracy": "None"

                        })


@app.route('/testupload')
def testUploadImage():
    return render_template('formUpload.html')


@app.route('/api/login', methods=['GET', 'POST'])
def Login():

    try:
        content = request.get_json()
    except Exception as e:
        logging.exception(str(e))
        return errorForLoginJsonFormat("didnt receive a json file ")

    if content is None:
        return errorForLoginJsonFormat("didnt receive a json file ")
    username = content.get('username')
    if username is None:
        return errorForLoginJsonFormat("username is not found in json file ")
    password = content.get('password')
    if password is None:
        return errorForLoginJsonFormat("username is not found in json file ")
    CheckIfUserExist = PatientController.getPatientByUserNamepassword(username, password)
    if CheckIfUserExist:
        return jsonify({
            'user_found': '1',
            'error': 'nothing'

        })
    else:
        return jsonify({
            'user_found': '0',
            'error': 'nothing'

        })


@app.route('/api/createaccount', methods=['GET', 'POST'])
def createAccount():
    try:
        # check if we got a json file
        content = request.get_json()
    except Exception as e:
        return jsonify({
            'successful': '0',
            'error': '1',
            'error_message': 'didnt receive a json file '

        })
    try:
        username = content.get('username')
        if username is None:
            return errorForCreateAccountJsonFormat(2, "json file doesn't have username")
        password = content.get('password')
        if password is None:
            return errorForCreateAccountJsonFormat(3, "json file doesn't have password")
        firstName = content.get('first_name')
        if firstName is None:
            return errorForCreateAccountJsonFormat(4, "json file doesn't have firstName")
        lastName = content.get('last_name')
        if lastName is None:
            return errorForCreateAccountJsonFormat(5, "json file doesn't have lastName")
        age = content.get('age')
        if age is None:
            return errorForCreateAccountJsonFormat(6, "json file doesn't have age")
        email = content.get('email')
        if email is None:
            return errorForCreateAccountJsonFormat(7, "json file doesn't have email")
        phone = content.get('phone')
        if phone is None:
            return errorForCreateAccountJsonFormat(8, "json file doesn't have phone")

        checkUserFoundinDataBase = PatientController.getPatientByUserName(username)
        if checkUserFoundinDataBase:
            return errorForCreateAccountJsonFormat(9, "Username already exist")
        p = Patient(username, password, firstName, lastName, age, email, phone)
        PatientController.addPatientt(p)
        return jsonify({
            'successful': '1',
            'error': '0',
            'error_message': "None"

        })
    except Exception as e:
        logging.exception(str(e))
        return jsonify({
            'successful': '0',
            'error': '99',
            'error_message': "Exception : " + str(e)

        })


def errorForCreateAccountJsonFormat(errorNum, errorMessage):
    return jsonify({
        'successful': '0',
        'error': str(errorNum),
        'error_message': str(errorMessage)

    })


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/exit', methods=['POST', 'GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def errorForLoginJsonFormat(errorString):
    return jsonify({
        'user_found': '0',
        'error_message': str(errorString)

    })


app.run(host='0.0.0.0')
