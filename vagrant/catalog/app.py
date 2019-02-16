#from and imports section
#flask imports 
from flask import (Flask,
request, render_template, url_for, redirect,
make_response, flash, jsonify)
from flask import session as login_session

#sqlalchemy imports
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
#database imports *
from db_setup import Base, User, Category, Items

#oauth imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
#general imports
import requests, string, httplib2, json, random, datetime


app = Flask(__name__)


#gconnect CLIENT_ID









#session db, connect to db and create session
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()





#login method
@app.route('/login')



#gconnect
@app.route('/gconnect', methods=['POST'])




#helper method




#gdisconect
@app.route('/gdisconnect')



#homepage
@app.route('/')
@app.route('/catalog')



#items
@app.route('/catalog/<path:category_name>/items')




#item
@app.route('/catalog/<path:category_name>/<path:item_name>')




#crud Category:
#add category
@app.route('/catalog/addcategory', methods=['GET', 'POST'])
#make sure user loged in ???


#edit category
@app.route('/catalog/<path:category_name>/edit', methods=['GET', 'POST'])
#make sure user loged in ???



#delete category
@app.route('/catalog/<path:category_name>/delete', methods=['GET', 'POST'])
#make sure user loged in ???




#crud item:
#add item
@app.route('/catalog/add', methods=['GET', 'POST'])
#make sure user loged in ???




#edit item
@app.route('/catalog/<path:category_name>/<path:item_name>/edit',
                            methods=['GET', 'POST'])
#make sure user loged in ???



#delete item
@app.route('/catalog/<path:category_name>/<path:item_name>/delete',
                            methods=['GET', 'POST'])
#make sure user loged in ???






#apis







#if main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)








