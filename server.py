from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import datetime
import json
import time
import gunicorn

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/mapita')
def mapita():
    return render_template('mapita.html')

@app.route('/mapa2')
def mapa2():
    return render_template('mapa2.html')

@app.route('/mapa3')
def mapa3():
    return render_template('mapa3.html')

@app.route('/cvs')
def cvs():
    return render_template('cvs.html')

@app.route('/groom')
def groom():
    return render_template('groom.html')

@app.route('/pc')
def pc():
    return render_template('pc.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route("/register", methods =["GET"])
def  register_user2():
    return render_template("register.html " )



@app.route("/register", methods =["POST"])
def  register_user():
    c = json.loads(request.form["value"])
    user = entities.User(
        username=c["username"],
        name=c["name"],
        fullname=c["full name"],
        password=c["password"]
    )
    session = db.getSessin(engine)
    session.add(user)
    session.comit()
    return render_template("register.html")

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    return "Deleted User"

@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(name="David", fullname="Lazo", password="1234", username="qwerty")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"



@app.route("/authenticate", methods = ["POST"])
def authenticate():
    username= request.form["username"]
    password =request.form["password"]
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.username == username
    ).filter(
        entities.User.password ==password
    ).first()

    if user != None:
        session ["usuario"] = username;
        return render_template('shop.html')
    else:
        return render_template('index.html')

@app.route('/current', methods = ['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == session['logged_user']).first()
    return Response(json.dumps(user,cls=connector.AlchemyEncoder),mimetype='application/json')

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(debug=True,port=8000, threaded=True, host=('127.0.0.1'))
