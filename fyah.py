# import os

from flask import Flask, render_template, url_for, request, redirect, flash, session
from functools import wraps
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail config
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv(),#'sinclair.python@gmail.com',
    MAIL_PASSWORD = os.getenv(),
    MAIL_DEFAULT_SENDER = ('Fyah Events ©', os.getenv()),#'sinclair.python@gmail.com'), #('NAME OR TITLE OF SENDER', 'SENDER EMAIL ADDRESS')
    MAIL_MAX_EMAILS = 25
))

mail = Mail(app)

# set session secret key
app.secret_key = os.getenv()#"Sinclair"

# redirect to login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to sign in first')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        name = request.form.get("name")
        number = request.form.get("number")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        confirm = request.form.get("confirm")
        sub = request.form.get("subject")
        content = request.form.get("message_content")

        # this will be the email address that the messages will be sent to
        myEmail = os.getenv()#'fyahevents@gmail.com'

        if '@' not in email:
            error = 'Your message did not send. Please provide a valid email'
            return render_template('home.html', error=error)
        elif '@' not in email and '@' not in confirm:
            error = 'Please provide a valid email'
            return render_template('home.html', error=error)
        elif myEmail == confirm:
            if '@' not in email and '@' not in confirm:
                error = 'Please provide a valid email'
                return render_template('home.html', error=error)
        else:
            msg = Message(f'{sub}', recipients=[myEmail])
            msg.html = f"<p>From: {name}<br>Email: {email}<br>Contact Number: {number}<br>Mobile Number: {mobile}<br><br>{content}<br><br>To send a response, please click <b><a href='https://fyahevents.onrender.com/admin'>here</a></b>.</p>"

            with app.open_resource('fyah_events_logo.jpg') as logo:
                msg.attach('fyah_events_logo.jpg', 'image/jpeg', logo.read())

            mail.send(msg)

            flash(f'Thank you {name} for your message, Fyah Events © will respond to you soon!')
            return redirect(url_for('home'))

@app.route('/sendSMS', methods=['GET', 'POST'])
def sendSMS():
    if request.method == 'GET':
        return render_template('sendSMS.html')
    else:
        name = request.form.get('name')
        num = request.form.get('number')
        txt = request.form.get('txt_content')

        from clockwork import clockwork
        api = clockwork.API('9347aab600cbf889dac37eafbbff00c708a65e52',)	# this has been left blank to protect API identity

        message = clockwork.SMS(
		    to = '447711906690',
            message = f'From: {name}\nNumber: {number}\n\n{txt}\n\nFyah Events',
		    from_name='Fyah Events') # from_name can max 11 characters long.

        response = api.send(message)

        if response.success:
            flash(f"Thanks {name}, your text was successfully sent! You will recieve a qoute from Fyah Events © soon.")
            return render_template('sendSMS.html')
        else:
            error = "Something went wrong, please try again!"
            return render_template('sendSMS.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    admin = request.form.get("username")
    admin_pw = request.form.get("password")
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if admin == 'admin' and admin_pw == '1234':
        # if admin == os.getenv('ADMIN') and admin_pw == os.getenv('GMAIL_PW'):
            session['logged_in'] = True
            flash(f'Welcome back Fyah Events ©!')
            return redirect(url_for('admin'))
        else:
            error = "Invalid username and/or password.  Only Fyah Events © has access to login."
    return render_template('login.html', error=error)

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('See you soon Fyah Events ©!')
    return redirect(url_for('home'))

@app.route('/email', methods=['GET', 'POST'])
@login_required
def email():
    if request.method == 'GET':
        return render_template('email.html')
    else:
        person = request.form.get("sendTo")
        email = request.form.get("emailTo")
        sub = request.form.get("sub")
        content = request.form.get("email_content")
        if '@' not in email:
            error = 'Your message did not send. Please provide a valid email'
            return render_template('email.html', error=error)
        else:
            msg = Message(f'{sub}', recipients=[email.lower()])
            msg.html = f"<p>Hi {person}!</p><br><p>Thank you for showing interest in Fyah Events©.</p><br><p>{content}</p><br><p>Kind regards</p><br><p><a href='https://fyahevents.onrender.com/'>Fyah Events ©</a></b></p>"

            with app.open_resource('fyah_events_logo.jpg') as logo:
                msg.attach('fyah_events_logo.jpg', 'image/jpeg', logo.read())
            mail.send(msg)
            flash(f'Your email has been sent to {person}!')
    return render_template('admin.html')

@app.route('/sms', methods=['GET', 'POST'])
@login_required
def sms():
    if request.method == 'GET':
        return render_template('sms.html')
    else:
        name = request.form.get('name')
        num = request.form.get('number')
        txt = request.form.get('txt_content')

        # convert to international UK number format
        list_num = list(num)
        list_num[0] = '44'
        new_num = "".join(list_num)

        from clockwork import clockwork
        api = clockwork.API(os.getenv(),)#'9347aab600cbf889dac37eafbbff00c708a65e52',)	# this has been left blank to protect API identity

        message = clockwork.SMS(
		    to = f'{new_num}',
            message = f'Hi {name}!\n\n{txt}\n\nFyah Events',
		    from_name='Fyah Events') # from_name can max 11 characters long.

        response = api.send(message)

        if response.success:
            flash(f"Your text to {name} was successfully sent!")
            return render_template('admin.html')
        else:
            error = "Something went wrong, please try again!"
            return render_template('sms.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
