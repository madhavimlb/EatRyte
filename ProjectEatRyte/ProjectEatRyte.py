from flask import Flask, render_template,request
from NutritionReqCalculatorForm import *
from flask import flash
from nutritionAPI import *
from flask_wtf.csrf import CSRFProtect
from calculateActualNutrition import *


app = Flask(__name__)

global index

@app.route('/')
def homepage():
    print('inside static page')
    return render_template('index.html')


@app.route('/enterNutriDetails',methods=['POST'])
def enterNutritionDetails():
    print('okokokokoko')
    if request.method == 'POST':
        index=1
        sex = request.form.get('sex')
        print(sex)
        weight = request.form.get('weight')
        print (weight)
        height = request.form.get('height')
        print (height)
        age = request.form.get('age')
        print (age)
        physicalActivity = request.form.get('physical activity')
        print(physicalActivity)
        nutrition = actualNutrition(sex,height,weight,age,physicalActivity)
        cal = nutrition.calulateCalorieNeeds()
        print("Calories : %f" %cal)
        pro = nutrition.calulateProteinNeeds()
        print("Protiens : lower limit %f , upper limit %f" % (pro[0] ,pro[1]))
        carbs = nutrition.calculateCarbsNeeds()
        print("Carbs : lower limit %f , upper limit %f" % (carbs[0], carbs[1]))
        fats = nutrition.calculateFasNeeds()
        print("fats :  %f" % fats)
        #Session["Calories"] = cal
        return render_template('Main.html',cal=cal,pro_l=pro[0],pro_u=pro[1],carbs_u=carbs[0],carbs_l=carbs[1],fats=fats)
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
    app.debug = True
    app.run()




