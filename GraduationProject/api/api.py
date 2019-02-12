# hassan comments
# jsonify() -> allows us to convert lists and dictionaries to JSON format
#@app.route((path), methods=['GET']) -> when routeing to it 





#
import flask
import sys
from flask import request, jsonify
from flask import abort
from flask import render_template
from werkzeug.utils import secure_filename
import os
import requests
from flask import Flask, redirect, url_for
from werkzeug.utils import secure_filename

# configration part #
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = 'E:\\python\\api\\Images'

######
# check if an extension is valid and that uploads the file and redirects the user to the URL for the uploaded file
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''
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
@app.route('/api/v1/imageurl', methods=['GET'])
def getImageAndRunScript():
	serverImageUrl =''
	if 'url' in request.args:
		localImageUrl = str(request.args['url'])
		files = {'files': open(localImageUrl, 'rb')}
		r = requests.post('http://127.0.0.1:5000/upload', files=files)
		serverImageUrl = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
	else :
		print('false', file=sys.stderr)
		return abort(404)
	import helloWorld as importedScript
	return importedScript.helloworld()
@app.route('/upload', methods= ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        image = request.files['files']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        return '200'
    else:
        return 'Upload Page'


	

app.run()


