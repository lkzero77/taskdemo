# Welcome to Task!

This is demo for ticket web application on python (flask framework) and vue frontend.

Download: https://github.com/lkzero77/taskdemo/blob/master/Test%20Demo.pptx

# Setup
git clone https://github.com/lkzero77/taskdemo.git

cd taskdemo

# Install virtualenv on window

python -m venv venv

# Active virtualenv

venv/bin/activate

pip install -r requirements.txt

flask run

# Config database
app.py

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tasks'

import database: tasks.sql


# Login page

admin: admin@admin.com | pass:123456
user: test@test.com | pass:123456