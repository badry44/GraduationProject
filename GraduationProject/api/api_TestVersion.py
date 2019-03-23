# hassan comments
# jsonify() -> allows us to convert lists and dictionaries to JSON format
# @app.route((path), methods=['GET']) -> when routeing to it


#
import flask
import sys
from flask import request, jsonify, render_template, flash, redirect, url_for, session, logging
from flask import abort
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import logging
import os
import requests
from werkzeug.utils import secure_filename


# configration part #

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '\\Images'
#   app.config['UPLOAD_FOLDER'] = 'C:\\Users\\ebrahem1\\Desktop\\GP\\GP\\api' + '\\Images'
app.config["MYSQL_DATABASE_USER"] = 'apiAdmin'
app.config["MYSQL_DATABASE_PASSWORD"] = 'root'
app.config["MYSQL_DATABASE_DB"] = 'skin diseases'
app.config["MYSQL_DATABASE_HOST"] = 'localhost'
ImageName = ''
logging.basicConfig(filename='app.log', format='%(asctime)s : -%(message)s',filemode = 'a')
mysql = MySQL()
mysql.init_app(app)
######
# check if an extension is valid and that uploads the file and redirects the user to the URL for the uploaded file
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


@app.route('/', methods=['GET'])
def home():
    return '''<h1>skin diseases</h1>
<p>A prototype API </p>'''
@app.errorhandler(404)
def page_not_found(e):
    return "this is error"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return abort(404)  # "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/uploadimage', methods=['GET', 'POST'])
def getImageAndRunScript():
    try:
        serverImageUrl = ''
        if request.method == 'POST':
            file = request.files['pic']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            serverImageUrl =  os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            # print('false', file=sys.stderr)
            return abort(404)
        #return jsonify({"error": "Nothing"})
        
        modelUrl = os.getcwd() + "\\other\\trainedModel.model"
        labelUrl =  os.getcwd() +"\\other\\labels.pickle"
        from other import  Prediction as importedScript
        classResult , accuracyResult = importedScript.predict(serverImageUrl,modelUrl,labelUrl)
        return jsonify({"error": "Nothing",
                        "class": str(classResult),
                        "accuracy": str(accuracyResult)
                        })
    except Exception as e:
        logging.exception(str(e))
        return jsonify({"error": str(e),
                        "class":"None",
                        "accuracy":"None"
                        
                        })


@app.route('/test')
def testy():
    try : 
        exep = 5/0
    except Exception as e: 
        logging.exception(str(e))
    return "zzz"
    


@app.route('/testupload')
def testUploadImage():
    return render_template('formUpload.html')


@app.route('/test', methods=['POST'])
def aut():
    username = request.form['u']
    password = request.form['p']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM profile")
    data = cursor.fetchone()
    if data is None:
        return "None"
    else:
        return str(type(data))


@app.route('/api/login', methods=['GET', 'POST'])
def Login():
    try:
        # check if we got a json file
        # print request.headers
        # return  request.get_data()
        # return jsonify(request.get_json(force=True))
        content = request.get_json()
    except:
        return jsonify({
            'user_found': '0',
            'error_message': 'didnt receive a json file '

        })
    if content is None:
        return jsonify({
            'user_found': '0',
            'error_message': 'didnt receive a json file '

        })
    username = content.get('username')
    if username is None:
        return jsonify({
            'user_found': '0',
            'error_message': 'username is not found in json file'

        })

    password = content.get('password')
    if password is None:
        return jsonify({
            'user_found': '0',
            'error_message': 'password is not found in json file '

        })

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM profile WHERE username = '" +
                   username+"' and password = '"+password+"'")
    data = cursor.fetchone()

    if data is None:
        return jsonify({
            'user_found': '0',
            'error': 'nothing'

        })
    else:
        return jsonify({
            'user_found': '1',
            'error': 'nothing'

        })


@app.route('/api/createaccount', methods=['GET', 'POST'])
def createAccount():
    try:
        # check if we got a json file
        content = request.get_json()
    except:
        return jsonify({
            'successful': '0',
            'error': '1',
            'error_message': 'didnt receive a json file '

        })
    try:
        username = content.get('username')
        if username is None:
            return errorForCreateAccount(2, "json file doesn't have username")
        password = content.get('password')
        if password is None:
            return errorForCreateAccount(3, "json file doesn't have password")
        firstName = content.get('first_name')
        if firstName is None:
            return errorForCreateAccount(4, "json file doesn't have firstName")
        lastName = content.get('last_name')
        if lastName is None:
            return errorForCreateAccount(5, "json file doesn't have lastName")
        age = content.get('age')
        if age is None:
            return errorForCreateAccount(6, "json file doesn't have age")
        email = content.get('email')
        if email is None:
            return errorForCreateAccount(7, "json file doesn't have email")
        phone = content.get('phone')
        if phone is None:
            return errorForCreateAccount(8, "json file doesn't have phone")
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM profile WHERE username = '"+username+"'")
        checkUserFound = cursor.fetchone()
        if checkUserFound is not None:
            return errorForCreateAccount(9, "Username is exists")
        insertUserCommand = (
            "INSERT INTO profile (username, password,first_name, last_name,age,email,phone) VALUES(%s, %s ,%s, %s, %s, %s, %s)")
        insertUserValues = (str(username), str(password), str(firstName),
                            str(lastName), int(age), str(email), str(phone))
       # insertUserValues = ('badry1','123','z','z',22,'a@a.a','111111')
        cursor.execute(insertUserCommand, insertUserValues)
        connection.commit()
        return jsonify({
            'successful': '1',
            'error': '0',
            'error_message': "None"

        })
    except Exception as e:
        return jsonify({
            'successful': '0',
            'error': '99',
            'error_message': "Exception : " + str(e)

        })


def errorForCreateAccount(errorNum, errorMessage):
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

@app.route('/exit', methods=['POST','GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
app.run(host='0.0.0.0', debug=True)
