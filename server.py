from flask import Flask, render_template, request
import pickledb as dbms
from werkzeug.exceptions import abort
from random import randint

db = dbms.load("customers.json", True)

app = Flask(__name__)

customers = ['Abhinav Vishnu', 'Kalpit Veerwal', 'Bill Gates']

for customer in customers:
    if str(db.get(customer)) == 'False':
        db.set(customer, randint(500,1000))

cust = dict()

for customer in customers:
    cust[customer] = db.get(customer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def view_customers():
    return render_template('customers.html', customers=customers)


@app.route('/transaction-page')
def transactionpage():
    return render_template("transactionpage.html", customers=cust, i=1)

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
        return "Sorry, your account has not enough balance :("
    else:
        db.set(fromx,(int(db.get(fromx))-int(amount)))
        db.set(to,(int(db.get(to))+int(amount)))
        return "Successful transfer :)"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=9000)
