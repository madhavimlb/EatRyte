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
        getNutritionfacts()
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()




