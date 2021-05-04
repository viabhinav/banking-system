from flask import Flask, render_template, request, make_response
import pickledb as dbms
from werkzeug.exceptions import abort
from random import randint
import datetime
import random
import string
from captcha.image import ImageCaptcha as captchax
import requests
import os
import json

# PORTABILITY

false = "false"
null = "null"
true = "true"

# END PORTABILITY

db = dbms.load("customers.json", True)
captcha = dbms.load("captchadb.json", True)
logindb = dbms.load("logindb", True)
dbnames = dbms.load("dbnames", True)
captx = captchax(width=280,height=90)

app = Flask(__name__)

democustomers = ['Abhilasha Gupta', 'Arohi Kumar', 'Peter Gupta', 'Akash Kumar','Eliza Kumari','Gyan Sarita', 'Umesh Prasad','Siddhartha Raj','Nandini Arya','Ujwal Sahni']

if(list(db.getall()) == []):
    for customerx in democustomers:
        if str(db.get(customerx)) == 'False':
            db.set(customerx, randint(5000,10000))

customers = list(db.getall())

def captcha_gen(size=6, chars=string.ascii_uppercase + string.digits):
       return ''.join(random.choice(chars) for _ in range(size))

cust = dict()
bal = list()

for customer in customers:
    bal.append(db.get(customer))
    cust[customer] = db.get(customer)
    
def error(error, desc):
    resp = make_response(render_template("error.html", error=error, desc=desc))
    return resp

print(list(zip(cust,bal)))
@app.route('/')
def index():
    print(request.remote_addr)
    if request.cookies.get('user'):
        return render_template('index.html', usernamel=request.cookies.get('user'))
    else:
        return render_template('index.html')

@app.route('/customers')
def view_customers():
    if request.cookies.get('user'):
        return render_template('customers.html', customers=cust)
    else:
        return render_template('customers.html', customers=cust)


@app.route('/transaction-page', methods = ['GET','POST'])
def transactionpage():
    if (request.cookies.get("user")):
        capt = captcha_gen()
        tokenx = captcha_gen(size=12)
        captcha.set(tokenx, capt)
        captx.write(capt, 'static/'+tokenx+'.png')

        if (request.form.get('to')):
            return render_template("transactionpage.html", captcha = tokenx+'.png',token=tokenx,customers=customers, i=1,user=request.cookies.get("user"), h=request.form.get("to"),usernamel=request.cookies.get('user'))
        else:
            return render_template("transactionpage.html", captcha = tokenx+'.png',token=tokenx,customers=customers, i=1, user=request.cookies.get("user"),usernamel=request.cookies.get('user'))
    else:
        return error("You must login to do transactions.", "Login <a href = '/loginpage'>here</a>")
        
@app.route('/processtran',methods = ['POST'])
def processtrans():
    if (request.form.get('captcha') == captcha.get(request.form.get('token'))):
    
        fromx = ''
        to = ''
        for x in (request.form.get('from').split('+')):
            if x == (request.form.get('from').split('+'))[-1]:
                fromx += x
                pass
            else:
                fromx += (x + ' ')
        for x in (request.form.get('to').split('+')):
            print("x =" + x)
            if x == (request.form.get('to').split('+'))[-1]:
                to += x
                pass
            else:
                to += (x + ' ')
        print(fromx)
        print(to)
        amount = request.form.get('amount')
        if (str(db.get(fromx))=='False'):
            return render_template("noaccount.html", usernamel=request.cookies.get('user'))
        elif (db.get(fromx)<=int(amount)):
            return render_template("norembal.html", rembal = int(db.get(fromx)), usernamel=request.cookies.get('user'))
        elif (fromx==to):
            return render_template("nosameacc.html", usernamel=request.cookies.get('user'))
        else:
            db.set(fromx,(int(db.get(fromx))-int(amount)))
            db.set(to,(int(db.get(to))+int(amount)))
            return render_template("successfultrans.html", rembal = int(db.get(fromx)), usernamel=request.cookies.get('user'))
        os.remove("static\\"+request.form.get('token')+".png")
    else:
        return "Incorrect captcha"
        os.remove("static\\"+request.form.get('token')+".png")

@app.route('/info/<string:customerx>')
def custinfo(customerx):
    customern = customerx.replace('+', ' ')
    if request.cookies.get('user'):
        return render_template("customerinfo.html", name=customern, bal=db.get(customern), usernamel=request.cookies.get('user'))
    else:
        return render_template("customerinfo.html", name=customern, bal=db.get(customern), usernamel=request.cookies.get('user'))

@app.route('/login')
def login():
    resp = make_response(render_template("login.html", customers=customers))
    return resp

@app.route('/processlogin', methods = ['POST', 'GET'])
def processlogin():
    if request.form.get('username') and (request.form.get('username') in customers):
        print(request.remote_addr)
        print(str(requests.request("GET", "http://api.ipstack.com/"+str(request.remote_addr)+"?access_key=2d79f6560ebffd30224be6bc11624cbb").text))
        x = json.loads(str(requests.request("GET", "http://api.ipstack.com/"+str(request.remote_addr)+"?access_key=2d79f6560ebffd30224be6bc11624cbb").text))
        xX = request.form.get('username')+" "+captcha_gen()
        logindb.dcreate(xX)
        dbnames.set(request.form.get('username'),xX)
        logindb.dadd(xX, (str(x['longitude']),str(x['latitude'])))
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        resp = make_response(render_template("successfullogin.html"))
        print(request.form.get('username'))
        resp.set_cookie("user", request.form.get('username'), expires=expire_date)
        return resp
    else:
        abort(401)

@app.route('/createaccount', methods = ['POST'])
        
@app.route('/statuscode', methods = ['POST'])
def status():
    if(request.form.get('code')):
        abort(int(request.form.get('code')))
    else:
        return 'Enter a code'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
