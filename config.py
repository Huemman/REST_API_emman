from app import app
from flaskext.mysql import MySQL

credentials = {
    'username': 'root',
    'pass': '1234',
    'db': 'the_office',
    'host': 'localhost'
}


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = credentials['username']
app.config['MYSQL_DATABASE_PASSWORD'] = credentials['pass']
app.config['MYSQL_DATABASE_DB'] = credentials['db']
app.config['MYSQL_DATABASE_HOST'] = credentials['host']
mysql.init_app(app) 

