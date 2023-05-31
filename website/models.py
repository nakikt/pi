from . import db
from flask_login import UserMixin
import os
import base64
import pyotp


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(1))
    otp = db.Column(db.Boolean, nullable=False)
    otp_secret = db.Column(db.String(16))
    salt = db.Column(db.String(10))
    blockchain_id = db.Column(db.Integer)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')


    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(name= self.username, issuer_name="Land Registry")

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)