from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
auth = Blueprint("auth", __name__)
salt = str(secrets.token_urlsafe(10))
pepper = "M"


@auth.route("/login", methods=['GET', 'POST'])
def login():
    session.permanent = True
    #Creating user - use this code only once
    # new_user = User(username="a", password=generate_password_hash(f'{salt}12345{pepper}', method='sha256'), otp=False, salt = salt, role= "A")
    # db.session.add(new_user)
    # db.session.commit()
    # login_user(new_user, remember=True)
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        otp_verification = request.form.get("p")
        if '"' in username or '"' in password:
            return "Error, pls don't try to hack our page :)"
        user = User.query.filter_by(username=username).first()

        if user:
            if otp_verification == "p" :
                if user.otp:

                    return redirect(url_for('auth.login'))
                    print("Nie logujesz się pierwszy raz")
                if check_password_hash(user.password, f'{user.salt}{password}{pepper}'):
                    login_user(user, remember=True)
                    return redirect(url_for('auth.two_factor_setup'))
                    #return redirect(url_for('views.home'))
                else:
                    flash('Password is incorrect.', category='error')
            else:
                otp = request.form.get("otp")
                otp = int(otp)
                if  check_password_hash(user.password, f'{user.salt}{password}{pepper}') and  user.verify_totp(otp):
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    print('Incorrect password or token.')

        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route('/twofactor')
@login_required
def two_factor_setup():

    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('two-factor-setup.html', user = current_user), 200

@auth.route('/qr')
@login_required
def qr():

    user = current_user
    print(user)
    # render qrcode for FreeTOTP
    # url = qrcode.make(user.get_totp_uri())
    # qrcode.make(user.get_totp_uri()).save("website/code.png")
    # stream = BytesIO()
    # url.svg(stream, scale=5)
    #return stream.getvalue(), 200
    return jsonify({"sukces"}), 200

@auth.route("/check" ,methods=['GET', 'POST'])
def check_otp():
    if request.method == 'POST':
        otp = request.form.get("otp")

