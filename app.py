from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS
import re
import hashlib
from datetime import datetime, timedelta

import logging
from logging.handlers import RotatingFileHandler
import os

# Gets or creates a logger
logger = logging.getLogger(__name__)  

# set log level
logger.setLevel(logging.WARNING)

# define file handler and set formatter
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/log.log',
                                    maxBytes=10240, backupCount=10)
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

app = Flask(__name__)

# config --> move to env
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tasks'

app.config['JWT_SECRET_KEY'] = 'tasks-secret'
app.config['SALT'] = 'Khoa@'

# call
CORS(app)
mysql = MySQL(app)
jwt = JWTManager(app)

# function utility
def check_user_exists(email, password):
    try:
        passwordHash = password + app.config['SALT']
        passwordHash = hashlib.md5(passwordHash.encode())
        c = mysql.connection.cursor()
        c.execute('''SELECT id, username, email, password, role FROM users WHERE email = %s AND password = %s''', (email, passwordHash.hexdigest()))
        data = c.fetchone()
        c.close()
        return data
    except:
        return jsonify({"msg": "Error: unable to fecth data"}), 400

def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False

def validate_status(status):
    list_status = ['waiting','working','issued','processing','done']
    if status in list_status:
        return True
    return False

# Not found
@app.errorhandler(404) 
def not_found(e):
    logger.error(str(e))
    return render_template("404.html")

# route signin - signout - signup
@app.route('/')
@app.route('/signin')
@app.route('/signout')
def index():
    return render_template('index.html')

@app.route('/api/v1/signin', methods=['POST'])
def signin():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not validate_email(email):
        return jsonify({"msg": "Invalid email"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = check_user_exists(email, password)
    if not user:
        return jsonify({"msg": "Bad email or password"}), 401

    info = {
        'id': user[0],
        'username': user[1],
        'role': user[4]
    }

    expires = timedelta(days=365)
    token = create_access_token(identity=info, expires_delta=expires)

    return jsonify(token=token, role=user[4], username= user[1]), 201

@app.route('/api/v1/signout')
@jwt_required
def signout():
    return jsonify({"msg": "Sign out successfull!"}), 200

@app.route('/api/v1/signup', methods=['POST'])
def signup():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        repassword = request.json.get('repassword', None)
        email = request.json.get('email', None)

        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400
        if not repassword:
            return jsonify({"msg": "Missing Repassword parameter"}), 400
        if password != repassword:
            return jsonify({"msg": "Password and Repassword are difference"}), 400
        if not email:
            return jsonify({"msg": "Missing email parameter"}), 400
        if not validate_email(email):
            return jsonify({"msg": "Invalid email"}), 400
        
        passwordHash = password + app.config['SALT']
        passwordHash = hashlib.md5(passwordHash.encode())

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO users(id, username, password, email, created_at) VALUES ('',%s,%s,%s, NOW())''', (username, passwordHash.hexdigest(), email))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Sign up successfull!"}), 200
    except Exception as e:
        return jsonify({"msg": "Sign up not successfull!"}), 400
	
@app.route('/api/v1/get-user-from-token', methods=['GET'])
@jwt_required
def get_user_from_token():
    cur_user = get_jwt_identity()
    return jsonify(signed_in_as=cur_user), 200

# User manager
@app.route('/api/v1/user/list')
@jwt_required
def get_all_users():
    cur_user = get_jwt_identity()
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''SELECT id, username, email, role FROM users WHERE isActived = %s''', [1])
        
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
    except:
        return jsonify({"msg": "Error: unable to fecth data"}), 400

    cursor.close()  
    return jsonify(data=data), 200

# Tickets manager
@app.route('/api/v1/ticket/list')
@jwt_required
def get_all_tickets():
    cur_user = get_jwt_identity()
    cursor = mysql.connection.cursor()
    try:
        if cur_user['role'] == 'admin':
            cursor.execute('''SELECT t1.id, t1.assign_user_id, t1.name, t1.description, UNIX_TIMESTAMP(t1.date_of_submission) AS date_of_submission, t1.status, t1.isShow, UNIX_TIMESTAMP(t1.created_at) AS created_at, t1.created_by, t1.updated_by, UNIX_TIMESTAMP(t1.updated_at) AS updated_at, t2.email, t2.username, t2.role FROM tickets AS t1 LEFT JOIN users AS t2 ON t1.assign_user_id = t2.id''')
        else:
            cursor.execute('''SELECT t1.id, t1.assign_user_id, t1.name, t1.description, UNIX_TIMESTAMP(t1.date_of_submission) AS date_of_submission, t1.status, t1.isShow, UNIX_TIMESTAMP(t1.created_at) AS created_at, t1.created_by, t1.updated_by, UNIX_TIMESTAMP(t1.updated_at) AS updated_at, t2.email, t2.username, t2.role FROM tickets AS t1 LEFT JOIN users AS t2 ON t1.assign_user_id = t2.id WHERE t1.assign_user_id = %s AND t1.isShow = %s''', (cur_user['id'], 1))
        
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
    except:
        return jsonify({"msg": "Error: unable to fecth data"}), 400

    cursor.close()  
    return jsonify(data=data), 200

@app.route('/api/v1/ticket/view/<id>')
@jwt_required
def view_ticket(id):
    try:
        val = int(id)
    except ValueError:
        return jsonify({"msg": "Not found"}), 404

    cur_user = get_jwt_identity()
    cursor = mysql.connection.cursor()
    try:
        if cur_user['role'] == 'admin':
            cursor.execute('''SELECT name, description, status, isShow FROM tickets WHERE id = %s''', [val])
        else:
            cursor.execute('''SELECT name, description, status, isShow FROM tickets WHERE assign_user_id = %s AND id = %s''', (cur_user['id'], val))
        data = cursor.fetchone()
    except:
        return jsonify({"msg": "Error: unable to fecth data"}), 400

    if not data:
        return jsonify({"msg": "Not found"}), 404

    cursor.close()
    return jsonify(id=val, name=data[0], description=data[1], status=data[2], isShow=data[3]), 200

@app.route('/api/v1/ticket/add', methods=['POST'])
@jwt_required
def add_ticket():
    name = request.json.get('name', None)
    description = request.json.get('description', None)
    date_of_submission = request.json.get('date_of_submission', None)
    date_of_submission_format = None if not date_of_submission else datetime.fromtimestamp(date_of_submission)
    assign_user_id = request.json.get('assign_user_id', None)

    if not name:
        return jsonify({"msg": "Missing name parameter"}), 400
    if not description:
        return jsonify({"msg": "Missing description parameter"}), 400

    cur_user = get_jwt_identity()
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''INSERT INTO tickets(id, assign_user_id, name, description, date_of_submission, created_at, created_by) VALUES ('',%s,%s,%s,%s,NOW(),%s)''', (assign_user_id, name, description, date_of_submission_format, cur_user['username']))
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
        return jsonify({"msg": "Create ticket not successfull!"}), 400

    cursor.close()
    return jsonify({"msg": "Create ticket successfull!"}), 200

@app.route('/api/v1/ticket/update/<id>', methods=['PUT'])
@jwt_required
def update_ticket(id):
    cur_user = get_jwt_identity()
    if cur_user['role'] != 'admin':
        return jsonify({"msg": "Not found"}), 404
    
    try:
        val = int(id)
    except ValueError:
        return jsonify({"msg": "Not found"}), 404

    name = request.json.get('name', None)
    description = request.json.get('description', None)
    date_of_submission = request.json.get('date_of_submission', None)
    date_of_submission_format = None if not date_of_submission else datetime.fromtimestamp(date_of_submission)
    assign_user_id = request.json.get('assign_user_id', None)
    status = request.json.get('status', None)
    isShow = request.json.get('isShow', None)

    if not isShow in (0,1):
        return jsonify({"msg": "Invalid isShow"}), 400
        
    if not validate_status(status):
        return jsonify({"msg": "Invalid status"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE tickets SET assign_user_id = %s, name = %s, description = %s, date_of_submission = %s, status = %s, isShow = %s, updated_by = %s, updated_at = NOW() WHERE id = %s''', (assign_user_id, name, description, date_of_submission_format, status, isShow, cur_user['username'], val))
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
        return jsonify({"msg": "Update ticket not successfull!"}), 400
    
    cursor.close()
    return jsonify({"msg": "Update ticket successfull!"}), 200

@app.route('/api/v1/ticket/update/<id>/status', methods=['PUT'])
@jwt_required
def update_ticket_status(id):
    try:
        val = int(id)
    except ValueError:
        return jsonify({"msg": "Not found"}), 404

    status = request.json.get('status', None)
    if not validate_status(status):
        return jsonify({"msg": "Invalid status"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE tickets SET status = %s WHERE id = %s''', (status, val))
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
        return jsonify({"msg": "Update ticket status not successfull!"}), 400
    # except Exception as e:
    #     return str(e)
    
    cursor.close()
    return jsonify({"msg": "Update ticket status successfull!"}), 200


# middleware
# @app.before_request
# def log_requests():
#     print('logging')
#     logger.debug('A debug message')
#     logger.info('An info message')
#     logger.warning('Something is not right.')
#     logger.error('A Major error has happened.')
#     logger.critical('Fatal error. Cannot continue')

# @app.after_request
# def after_request_func(response):
#     print("after_request is running!", jsonify(response))
#     logger.info(jsonify(response))
#     return response

@app.teardown_request
def teardown_request_func(error=None):
    cur_user = get_jwt_identity()
    if cur_user:
        logger.warning('User %s are working [%s] %s ', str(cur_user), request.method, request.full_path)
    if error:
        # Log the error
        logger.error(str(error))

if __name__ == '__main__':
	app.run(debug=True)