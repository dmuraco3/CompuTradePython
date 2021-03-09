import os
from subprocess import check_output
import flask
import flask_sqlalchemy
import flask_praetorian
import flask_cors
import dotenv
from dotenv import load_dotenv

import functools

import google.oauth2.credentials
import googleapiclient.discovery

load_dotenv()

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    description = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    bday = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    pfp = db.Column(db.Text)

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

# Initialize flask app
app = flask.Flask(__name__)
cors = flask_cors.CORS(app)
app.debug = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

# Initialize the flask-praetorian instance 
guard.init_app(app, User)

# Initialize a local database 
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Route for API
@app.route('/api/')
def home():
    return {"Hello": "World"}, 200

@app.route('/api/signup', methods=['POST'])
def signup():
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    email = req.get('email', None)
    password = req.get('password', None)
    if db.session.query(User).filter_by(username=username).count() < 1 and db.session.query(User).filter_by(email=email).count() < 1:
        print(username, ":", email, ":", password)
        res = check_output(f'cd .. && mkdir storage/{username}', shell=True)
        db.session.add(User(
          username=username,
          email=email,
          password=guard.hash_password(password),
          roles='user',
          description='free'
        ))
        print("added to session")
        db.session.commit()
        print("commited")
        user = guard.authenticate(email, password)
        print(res)
        ret = {'access_token': guard.encode_jwt_token(user)}
        return ret, 200
    else:
        return {'error': 'pick a different username'}, 401 
  
@app.route('/api/login', methods=['POST'])
def login():
    
    req = flask.request.get_json(force=True)
    email = str(req.get('email', None))
    password = str(req.get('password', None))
    user = guard.authenticate(email, password)
    ret = {'access_token': guard.encode_jwt_token(user), 'email': email}
    return ret, 200
  
@app.route('/api/refresh', methods=['POST'])
def refresh():
    
    print("refresh request")
    old_token = flask.request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200
  
@app.route('/api/protected')
@flask_praetorian.auth_required
def protected():
    return {"message": f'protected endpoint (allowed user {flask_praetorian.current_user().id})'}


@app.route('/api/settings', methods=['GET', 'POST'])
@flask_praetorian.auth_required
def settings():
    if flask.request.method == 'GET':
        to_return = {
            'username': f'{flask_praetorian.current_user().username}',
            'fname': f'{flask_praetorian.current_user().fname}',
            'lname': f'{flask_praetorian.current_user().lname}',
            'email': f'{flask_praetorian.current_user().email}',
            'bday': f'{flask_praetorian.current_user().bday}',
            'roles': f'{flask_praetorian.current_user().roles}'
        }
        return to_return, 200
    else:
        return {"error":"method not allowed"}, 400


@app.route('/api/dashboard')
@flask_praetorian.auth_required
def dashboard():
    try:
        projects = [f.path.split(f'../storage/{flask_praetorian.current_user().username}/')[1] for f in os.scandir(f'../storage/{flask_praetorian.current_user().username}/') if f.is_dir()]
        username = flask_praetorian.current_user().username
        pfp = flask_praetorian.current_user().pfp
        return {"projects": projects,
                "username": username,
                "pfp": pfp}, 200
    except:
        return {"projects": 0}, 200

@app.route('/api/dashboard/project/<project_name>', methods=["GET"])
@flask_praetorian.auth_required
def project(project_name):
    project_name = project_name
    with open(f'../storage/dylan/{project_name}/core.py', 'r') as fp:
        code = fp.readlines()
        fp.close()
    code = ''.join(code)
    return {"code": code}, 200


@app.route('/api/dashboard/newproject', methods=["POST"])
@flask_praetorian.auth_required
def newproject():
    print(flask.request.get_json(force=True))
    return {"ok": "ok"}, 200
    # req = flask.request.get_json(force=True)
    # project_name = req.get('project_name', None)
    # try:
    #     res = check_output(f'cd .. && mkdir storage/{flask_praetorian.current_user().username}/{project_name} &&  cd storage/{flask_praetorian.current_user().username}/{project_name} && touch app.py', shell=True)
    # except Exception:
    #     return flask.make_response({"error": "User Project Exists"})

@app.route('/api/dashboard/saveproject', methods=['POST'])
@flask_praetorian.auth_required
def saveproject():
    req = flask.request.get_json(force=True)
    project_name = req.get('projectName', None)
    value = req.get('value', None)
    value = value[0]
    try:
        with open(f'../storage/dylan/{project_name}/core.py', 'w') as fp:
            fp.write(value)
            fp.close()
        return {"thanks": "ack"}, 200
        

    except Exception:
        print(Exception)

