from main import *
from manage import *
from flask_mail import Mail, Message
import os
from twilio.rest import Client
import random
from datetime import datetime, timedelta

app.config.update(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='rajpatel14998@gmail.com',
        MAIL_PASSWORD='raj333patel'
    )
mail = Mail(app)
app.secret_key = os.environ.get("SECRET_KEY", "XYZ")
number = 0
mobile_number = 0


def send_mail(title, email, html):
    try:
        msg = Message(title, sender=("DRC System", "me@example.com"), recipients=[email])
        msg.html = html
        mail.send(msg)
        return msg
    except Exception as e:
        print(e)
    return

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/')
def default():
    return redirect(url_for('signup'))

@app.route('/user_signup', methods = ['POST'])
def signup_user():
    email = request.form['email']
    mobile = request.form['mobile']
    name = request.form['name']
    passwrd = request.form['pwd']
    if len(str(mobile)) <= 10:
        return make_response("<b>Please Enter valid number</b> Signup: <a href = 'signup'>Signup</a>")
    data = User.query.filter_by(phone_number=mobile).all()
    if data:
        return make_response("<b>Number is already Registered</b> Visit for Login: <a href = 'signin'>Login</a>")
    user = User(phone_number=mobile, name=name,
                        password=passwrd)
    db.session.add(user)
    db.session.commit()
    user_email = User_email(user_id=user.id, email=email)
    db.session.add(user_email)
    user_login = User_login(user_id=user.id, session=None)
    db.session.add(user_login)
    db.session.commit()

    html = "Welcome <b>"+ request.form['name'] + "</b> in <b>DRC System</b>. You have a successfully created account"
    send_mail("Welcome", email, html)
    session['is_user_login'] = True
    return make_response("<h1>Successfully Registered. You receive one welcome mail. Please visit <a target = '_blank' href = 'https://mail.google.com'>Gmail</a></h1>")


@app.route('/signin')
def signin():
    if "is_user_login" in session and session['is_user_login']:
        return render_template("home.html")
    return render_template("signin.html")

@app.route('/logout')
def logout():
    session = {}
    return render_template("signin.html")


@app.route("/user_signin", methods = ['POST'])
def signin_user():
    global mobile_number
    mobile_number = request.form['mobile']
    data = User.query.filter_by(phone_number=mobile_number).all()
    if data:
        user_login = User_login.query.filter_by(user_id=data[0].id).all()
        print(user_login)
        if user_login:
            if datetime.utcnow() < user_login[0].last_login:
                return make_response("<b>You will signin after 5 Minutes </b>")
    key = os.environ.get("TWILIO_SECRET_KEY", "ACfb3a006c0707c3514ea2a5a5c1313235")
    token = os.environ.get("TWILIO_SECRET_TOKEN", "c988bd441e483a9f9c978875614f1b64")
    client = Client(key, token)
    global number
    number = random.randint(1000, 9999)
    try:
        messages = client.messages.create(to=mobile_number,
                               from_="+13237725845",
                               body=number)
    except:
        return make_response("Something Went wrong")
    return render_template("otp.html", phone_number=mobile_number)


@app.route('/user_otp', methods = ['POST'])
def user_otp():
    try:
        otp_num = int(request.form['mobile'])
    except:
        return make_response("Please Enter the correct numeric number only")
    if "attempt_time" in session:
        session['attempt_time'] += 1
    else:
        session['attempt_time'] = 0
    print('attempt time', session['attempt_time'])
    if session['attempt_time'] >= 3:
        now = datetime.utcnow()
        next_login_time = now + timedelta(minutes=5)
        print(now)
        print(next_login_time)
        print(mobile_number)
        find_user = User.query.filter_by(phone_number=mobile_number).all()
        print("user found ", find_user)
        print("session is ", session)
        print(find_user[0].id)
        if find_user:
            # obj = User_login(user_id=find_user[0].id, session=int(session['user_number']),
            #            last_login=next_login_time)
            # db.session.update(obj)
            obj = User_login.query.filter_by(user_id=find_user[0].id).all()
            print('obj is ', obj)
            obj[0].last_login = next_login_time
            db.session.commit()
        session['attempt_time'] = 0
        return make_response("<h4>You will be blocked for 5 minutes</h4> <a href = '/signin'>Login</a>")
    else:
        if otp_num == number:
            session['is_user_login'] = True
            return render_template("home.html")
        return render_template('otp.html')
