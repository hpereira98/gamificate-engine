from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
from datetime import datetime
import jwt


class Admin(UserMixin, db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    realms = db.relationship('Realm', backref='author', lazy='dynamic')
    # falta premium

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id_admin, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        
        return Admin.query.get(id)


    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Admin {}>'.format(self.email)

    def get_id(self):
        return (self.id_admin)


class Realm(db.Model):
    id_realm = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(256), unique=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id_admin'))
    badges = db.relationship('Badge', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Realm {}>'.format(self.name)


class Badge(db.Model):
    id_badge = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    xp = db.Column(db.Integer)
    required = db.Column(db.Integer)
    realm_id = db.Column(db.Integer, db.ForeignKey('realm.id_realm'))
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id_reward'), nullable=True)

    def __repr__(self):
        return '<Badge {}>'.format(self.name)

class Reward(db.Model):
    id_reward = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __repr__(self):
        return '<Reward {}>'.format(self.name)

# intermediate table between User and Reward
class UserRewards(db.Model):
    __tablename__ = 'user_reward'
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_reward = db.Column(db.Integer, db.ForeignKey('reward.id_reward'), primary_key=True)
    redeem_date = db.Column(db.DateTime, nullable=True)
    reward = db.relationship("Reward")

# intermediate table between User and Badge
class UserBadges(db.Model):
    __tablename__ = 'user_badge'
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_badge = db.Column(db.Integer, db.ForeignKey('badge.id_badge'), primary_key=True)
    progress = db.Column(db.Integer)
    finished = db.Column(db.Boolean)
    finished_date = db.Column(db.DateTime)
    badge = db.relationship("Badge")

    def update_progress(self, progress):
        setattr(self, 'progress', self.progress + progress)
        # is self.badge a Badge object? needs testing
        badge = Badge.query.get(self.id_badge)
        if self.progress >= badge.required:
            setattr(self, 'finished', True)
            setattr(self, 'finished_date', datetime.now())

    def to_dict(self):
        data = {
            'id_badge': self.id_badge,
            'progress': self.id_badge,
            'finished': self.finished
        }
        if self.finished:
            data['finished_date'] = self.finished_date
        return data


class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(254), unique=True)
    total_xp = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    level = db.Column(db.Integer)
    realm_id = db.Column(db.Integer, db.ForeignKey('realm.id_realm'))
    badges = db.relationship("UserBadges")
    rewards = db.relationship("UserRewards")

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id_user,
            'username': self.username,
            'total_xp': self.total_xp,
            'active': self.active,
            'level': self.level,
            'realm_id': self.realm_id        
        }
        if include_email:
            data['email'] = self.email

        return data

    def from_dict(self, data):
        for field in ['username','email', 'total_xp', 'active', 'level', 'realm_id']:
            if field in data:
                setattr(self, field, data[field])

    def new_user(self, data):
        setattr(self, 'username', data['username'])
        setattr(self, 'email', data['email'])
        setattr(self, 'total_xp', 0)
        setattr(self, 'active', True)
        setattr(self, 'level', 1)
        setattr(self, 'realm_id', data['realm_id'])


class Standings(db.Model):
    realm_id = db.Column(db.Integer, db.ForeignKey('realm.id_realm'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    total_xp = db.Column(db.Integer)
    total_badges = db.Column(db.Integer)


class Level(db.Model):
    id_level = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Integer)
    b = db.Column(db.Integer)
    c = db.Column(db.Integer)
    realm_id = db.Column(db.Integer, db.ForeignKey('realm.id_realm'))

    def __repr__(self):
        return '<Level {}>'.format(self.realm_id)


# User-Loader Function
@login.user_loader
def load_admin(id):
    return Admin.query.get(int(id))
