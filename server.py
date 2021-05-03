from flask import Flask, render_template, request, make_response
import pickledb as dbms
from werkzeug.exceptions import abort
from random import randint
import datetime

db = dbms.load("customers.json", True)

app = Flask(__name__)

customers = ['Abhilasha Gupta', 'Arohi Kumar', 'Peter Gupta', 'Akash Kumar','Eliza Kumari','Gyan Sarita', 'Umesh Prasad','Siddhartha Raj','Nandini Arya','Ujwal Sahni']

for customer in customers:
    if str(db.get(customer)) == 'False':
        db.set(customer, randint(5000,10000))

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
    return render_template('index.html')

@app.route('/customers')
def view_customers():
    return render_template('customers.html', customers=cust)


@app.route('/transaction-page', methods = ['GET'])
def transactionpage():
    if (request.cookies.get("user")):
        if (request.args.get('to')):
            return render_template("transactionpage.html", customers=customers, i=1,user=request.cookies.get("user"), h=request.args.get("to"))
        else:
            return render_template("transactionpage.html", customers=customers, i=1, user=request.cookies.get("user"))
    else:
        return error("You must login to do transactions.", "Login <a href = '/loginpage'>here</a>")
        
@app.route('/processtran',methods = ['GET'])
def processtrans():
    fromx = ''
    to = ''
    for x in (request.args.get('from').split('+')):
        if x == (request.args.get('from').split('+'))[-1]:
            fromx += x
            pass
        else:
            fromx += (x + ' ')
    for x in (request.args.get('to').split('+')):
        print("x =" + x)
        if x == (request.args.get('to').split('+'))[-1]:
            to += x
            pass
        else:
            to += (x + ' ')
    print(fromx)
    print(to)
    amount = request.args.get('amount')
    if (str(db.get(fromx))=='False'):
        return render_template("noaccount.html")
    elif (db.get(fromx)<=int(amount)):
        return render_template("norembal.html", rembal = int(db.get(fromx)))
    elif (fromx==to):
        return render_template("nosameacc.html")
    else:
        db.set(fromx,(int(db.get(fromx))-int(amount)))
        db.set(to,(int(db.get(to))+int(amount)))
        return render_template("successfultrans.html", rembal = int(db.get(fromx)))

@app.route('/info/<string:customerx>')
def custinfo(customerx):
    customern = customerx.replace('+', ' ')
    return render_template("customerinfo.html", name=customern, bal=db.get(customern))

@app.route('/login')
def login():
    resp = make_response(render_template("login.html"))
    return resp

@app.route('/processlogin', methods = ['GET'])
def processlogin():
    if request.args.get('username') and (request.args.get('username') in customers):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        resp = make_response(render_template("successfullogin.html"))
        resp.set_cookie("user", request.args.get('username'), expires=expire_date)
        return resp
    else:
        abort(401)
        
@app.route('/statuscode', methods = ['GET'])
def status():
    if(request.args.get('code')):
        abort(int(request.args.get('code')))
    else:
        return 'Enter a code'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
