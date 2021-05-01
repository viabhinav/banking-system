from flask import Flask, render_template, request, make_response
import pickledb as dbms
from werkzeug.exceptions import abort
from random import randint

db = dbms.load("customers.json", True)
trans = dbms.load("transactions.json", True)

app = Flask(__name__)

customers = db.getall()

cust = dict()
bal = list()

transactions.dcreate("TRANS")

for customer in customers:
    bal.append(db.get(customer))
    cust[customer] = db.get(customer)

def refreshcust():
    customers = db.getall()
    for customer in customers:
        cust[customer] = db.get(customer)
    

print(list(zip(cust,bal)))
@app.route('/')
def index():
    #return render_template('index.html')
    resp = make_response(render_template('index.html'))
    return resp

@app.route('/customers')
def view_customers():
    return render_template('customers.html', customers=cust)


@app.route('/transaction-page')
def transactionpage():
    return render_template("transactionpage.html", customers=customers, i=1)

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
        return "Sorry, this account doesn't exist"
    elif (db.get(fromx)<int(amount)):
        return render_template("norembal.html", rembal = int(db.get(fromx)))
    else:
        db.set(fromx,(int(db.get(fromx))-int(amount)))
        db.set(to,(int(db.get(to))+int(amount)))
        return render_template("successfultrans.html", rembal = int(db.get(fromx)))


@app.route('/<string:name>')
def custinfo(name):
  if str(db.get(name))=='False':
      return render_template('custnotfound.html')
  else: 
      return render_template('customerinfo.html', cust=name, bal = db.get(name))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
