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
    MAIL_USERNAME = 'sinclairpythonakoto.mail@gmail.com',
    MAIL_PASSWORD = 'Python2020',
    MAIL_DEFAULT_SENDER = ('Fyah Events ©', 'sinclairpythonakoto.mail@gmail.com'), #('NAME OR TITLE OF SENDER', 'SENDER EMAIL ADDRESS')
    MAIL_MAX_EMAILS = 25
))

mail = Mail(app)

# set session secret key
app.secret_key = "Sinclair"

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
        email = request.form.get("email")
        # this will be the email address that the message will be sent to
        myEmail = 'design.build.apply@gmail.com'
        confirm = request.form.get("confirm")
        sub = request.form.get("subject")
        content = request.form.get("message_content")
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
            msg.html = f"<p>From: {name}<br>Email: {email}<br><br>Subject:{sub}<br><br>{content}<br><br>To send a response, please go click <b><a href='https://www.bondrobotics.tech'>here</a></b>.</p>"

            with app.open_resource('fyah_events_logo.jpg') as logo:
                msg.attach('fyah_events_logo.jpg', 'image/jpeg', logo.read())

            mail.send(msg)

            flash(f'Thank you {name} for your message, Fyah Events will respond to you soon!')
            return redirect(url_for('home'))
        # else:
        #     error = 'Your email did not match. Please provide matching emails'
        #     return render_template('home.html', error=error)

@app.route('/login')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
