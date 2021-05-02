from flask import Flask, render_template, request
import pickledb as dbms
from werkzeug.exceptions import abort
from random import randint

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

print(list(zip(cust,bal)))
@app.route('/')
def index():
    return render_template('index.html')

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
        return render_template("noaccount.html")
    elif (db.get(fromx)<int(amount)):
        return render_template("norembal.html", rembal = int(db.get(fromx)))
    else:
        db.set(fromx,(int(db.get(fromx))-int(amount)))
        db.set(to,(int(db.get(to))+int(amount)))
        return render_template("successfultrans.html", rembal = int(db.get(fromx)))

@app.route('/info/<string:customerx>')
def custinfo(customerx):
    customern = customerx.replace('+', ' ')
    return render_template("customerinfo.html", name=customern, bal=db.get(customern))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
