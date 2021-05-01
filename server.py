from Flask import flask
from flask import Flask, render_template
from threading import Thread
import pickledb as dbms
from werkzeug.exceptions import abort
import discord

db = dbms.load("playerbal.json", True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def view_customers():
    print('Hex')
def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
