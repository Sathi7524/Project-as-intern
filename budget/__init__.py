from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
app=Flask(__name__)
app.config['SECRET_KEY']="SpringmlsecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/springml'
db=SQLAlchemy(app)


from budget import routes
from budget import models