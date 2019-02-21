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
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
    APPLICATION_NAME = 'Item Catalog'







#session db, connect to db and create session
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()








#login method
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascij_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    return 'Session state is %s' % login_session['state']
    #later would be rendered to login.html



#user methods (helper functions)
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None





#gconnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    #Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Obtain authorzation code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        #Upgrade the auth code into a credentials objedt
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #token is valid?
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)

    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    #if there was an erroe in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doen't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content_Type'] = 'application/json'
        return response

    #store the access token in the session for later use
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    #Get user Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = request.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #Check if user exist, if no, make new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output




#gdisconect
@app.route('/gdisconnect')
def gdisconnect():
    #Disconnect a connected user
    access_token = login_session.get('access_token')# could be with 'credentials too
    if access_token is None:
        response = make_response(json.dumps('Currnt user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['states'] == '200':
        #reset user session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
        #could be redircted after the test is done to homepage/.

        else:
            #token given is Invalid
            response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     




#homepage
@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Items).order_by(desc(Items.date)).limit(3)
    return render_template('catalog.html', categories=categories, items = items)



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








