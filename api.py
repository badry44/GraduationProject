# hassan comments
# jsonify() -> allows us to convert lists and dictionaries to JSON format
#@app.route((path), methods=['GET']) -> when routeing to it 





#


import flask
import sys
from flask import request, jsonify
from flask import abort
from flask import render_template
app = flask.Flask(__name__)
app.config["DEBUG"] = True




@app.route('/', methods=['GET'])
def home():
    return '''<h1>This is Home</h1>
<p>Skin burns !.</p>'''
@app.errorhandler(404)
def page_not_found(e):
    return "this is error"
@app.route('/api/v1/imageurl', methods=['GET'])
def getImageAndRunScript():
	if 'url' in request.args:
		imageUrl = str(request.args['url'])
	else :
		return abort(404)
	import helloWorld as importedScript
	return importedScript.helloworld()
	

app.run()


