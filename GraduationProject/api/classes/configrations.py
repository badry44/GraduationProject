import os


def configApp(app, user='apiAdmin', password='root', database='skin diseases', host='localhost'):
    app.config['UPLOAD_FOLDER'] = os.getcwd() + '\\Images'
    app.config["MYSQL_DATABASE_USER"] = user
    app.config["MYSQL_DATABASE_PASSWORD"] = password
    app.config["MYSQL_DATABASE_DB"] = database
    app.config["MYSQL_DATABASE_HOST"] = host
