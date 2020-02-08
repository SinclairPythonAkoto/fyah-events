from flask import Flask, render_template, url_for, request, redirect, flash, session
from functools import wraps
from flask_mail import Mail, Message

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')



if __name__ == '__main__':
    app.run(debug=True)
