# hassan comments
# jsonify() -> allows us to convert lists and dictionaries to JSON format
#@app.route((path), methods=['GET']) -> when routeing to it 





#
import flask
import sys
from flask import request, jsonify ,render_template , flash , redirect ,url_for , session,logging
from flask import abort
#from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os
import requests
from werkzeug.utils import secure_filename

# configration part #

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = 'E:\\python\\api\\Images'
app.config["MYSQL_DATABASE_USER"] ='apiAdmin'
app.config["MYSQL_DATABASE_PASSWORD"] ='root'
app.config["MYSQL_DATABASE_DB"] ='skin diseases'
app.config["MYSQL_DATABASE_HOST"] ='localhost'
ImageName = ''
mysql = MySQL()
mysql.init_app(app)
######
# check if an extension is valid and that uploads the file and redirects the user to the URL for the uploaded file
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

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
        return abort(404)#"Error: No id field provided. Please specify an id."

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
@app.route('/api/imageurl', methods=['GET'])
def getImageAndRunScript():
	serverImageUrl =''
	if 'url' in request.args:
		localImageUrl = str(request.args['url'])
		files = {'files': open(localImageUrl, 'rb')}
		r = requests.post('http://127.0.0.1:5000/upload', files=files)
		print(ImageName," second!", file=sys.stderr)
		serverImageUrl = os.path.join(app.config['UPLOAD_FOLDER'], ImageName)
	else :
		print('false', file=sys.stderr)
		return abort(404)
	import helloWorld as importedScript
	return importedScript.helloworld(serverImageUrl)
@app.route('/upload', methods= ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        global ImageName
        image = request.files['files']
        ImageName = image.filename
        print(ImageName, file=sys.stderr)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        return '200'
    else:
        return 'Upload Page'
@app.route('/test')
def testy():
    return render_template('index.html')
@app.route('/test',methods = ['POST'])
def aut() :
    username = request.form['u']
    password = request.form['p']
    cursor = mysql.connect().cursor()
    cursor.execute ("SELECT * FROM profile")
    data = cursor.fetchone()
    if data is None : 
        return "None"
    else : 
        return str(type(data))

@app.route('/api/login',methods=['GET', 'POST'])
def Login() :
    try:
        # check if we got a json file
        content = request.get_json()
    except:
        return jsonify({
                'user_found' : '0',
                'error_message' : 'didnt receive a json file '
                
        })
    if content is None :
        return jsonify({
                'user_found' : '0',
                'error_message' : 'didnt receive a json file '
                
        })
    username = content.get('username')
    if username is None :
        return jsonify({
                'user_found' : '0',
                'error_message' : 'username is not found in json file'
                
        })
    
    password = content.get('password')
    if password is None :
        return jsonify({
                'user_found' : '0',
                'error_message' : 'password is not found in json file '
                
        })
    
        
    cursor = mysql.connect().cursor()
    cursor.execute ("SELECT * FROM profile WHERE username = '"+username+"' and password = '"+password+"'")
    data = cursor.fetchone()
    
    if data is None : 
        return jsonify({
                'user_found' : '0',
                'error' : 'nothing'
                
        })
    else:
        return jsonify({
                'user_found' : '1',
                'error' : 'nothing'
                
        })
@app.route('/api/createaccount',methods=['GET', 'POST'])
def createAccount() :
    try:
        # check if we got a json file
        content = request.get_json()
    except:
        return jsonify({
                'successful' : '0',
                'error' : '1',
                'error_message' : 'didnt receive a json file '
                
        })
    try:
        username = content.get('username')
        if username is None : 
            return  errorForCreateAccount(2,"json file doesn't have username")
        password = content.get('password')
        if password is None : 
            return  errorForCreateAccount(3,"json file doesn't have password")
        firstName = content.get('first_name')
        if firstName is None : 
            return  errorForCreateAccount(4,"json file doesn't have firstName")
        lastName = content.get('last_name')
        if lastName is None : 
            return  errorForCreateAccount(5,"json file doesn't have lastName")
        age = content.get('age')
        if age is None : 
            return  errorForCreateAccount(6,"json file doesn't have age")
        email = content.get('email')
        if email is None : 
            return errorForCreateAccount(7,"json file doesn't have email")
        phone = content.get('phone')
        if phone is None : 
            return  errorForCreateAccount(8,"json file doesn't have phone")
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute ("SELECT * FROM profile WHERE username = '"+username+"'")
        checkUserFound = cursor.fetchone()
        if checkUserFound is not None :
            return  errorForCreateAccount(9,"Username is exists")
        insertUserCommand =("INSERT INTO profile (username, password,first_name, last_name,age,email,phone) VALUES(%s, %s ,%s, %s, %s, %s, %s)")
        insertUserValues = (str(username),str(password),str(firstName),str(lastName),int(age),str(email),str(phone))
       # insertUserValues = ('badry1','123','z','z',22,'a@a.a','111111')
        cursor.execute (insertUserCommand,insertUserValues)
        connection.commit()
        return jsonify({
                'successful' : '1',
                'error' : '0',
                'error_message' : "None"
                    
                })
    except Exception as e:
        return jsonify({
                'successful' : '0',
                'error' : '99',
                'error_message' : "Exception : " + str(e)
                
        })


def errorForCreateAccount(errorNum , errorMessage) : 
    return jsonify({
                'successful' : '0',
                'error' : str(errorNum),
                'error_message' : str(errorMessage)
                
        }) 
        
    
app.run()


