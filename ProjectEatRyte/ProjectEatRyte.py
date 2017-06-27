from flask import Flask, render_template,request
from nutritionAPI import *
app = Flask(__name__)


@app.route('/')
def homepage():
    print('inside static page')
    return render_template('index.html')

@app.route('/login')
def login():
    pass

@app.route('/getNutrition', methods=['POST'])
def getNutrtion():
    print('inside get nutrition')
    if request.method=='POST':
        useritem = request.form.get('itemName')
        userBrand=request.form.get('brand')
        userquantity = request.form.get('quantity')
        usermealtype= request.form['usermealtype']
        getNutritionfacts(useritem ,userBrand, userquantity,usermealtype)
        return render_template('Main.html')

if __name__ == '__main__':
    app.debug = True
    app.run()




