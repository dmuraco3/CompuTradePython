import os
import flask
import flask_sqlalchemy
import flask_praetorian
from dotenv import load_dotenv

load_dotenv()
db = flask_sqlalchemy.SQLAlchemy()
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

app = flask.Flask(__name__)


guard = flask_praetorian.Praetorian()
app.config['SECRET_KEY'] = '123'

guard.init_app(app, User)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



# add user
with app.app_context():
    db.create_all()
    if db.session.query(User).filter_by(username='dylan').count() < 1:
        db.session.add(User(
            username = 'dylan',
            password = guard.hash_password('strongpassword'),
            fname = 'Dylan',
            lname = 'Muraco',
            description = 'admin',
            email = 'admin@admin.com',
            bday = '06/15/2004',
            roles = 'admin',
            pfp = '/default/iconfinder_man_male_avatar_portrait_4043260.svg'
            ))
    else: 
        print("exists")
    db.session.commit()
