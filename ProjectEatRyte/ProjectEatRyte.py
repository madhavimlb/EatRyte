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
        cal = float("{0:.2f}".format(cal))
        print("------------------tyoe cal ---------------------")
        print(type(cal))
        print("Calories : %f" %cal)
        pro = nutrition.calulateProteinNeeds()
        pro_l= float("{0:.2f}".format(pro[0]))
        pro_u = float("{0:.2f}".format(pro[1]))
        print("Protiens : lower limit %f , upper limit %f" % (pro[0] ,pro[1]))
        carbs = nutrition.calculateCarbsNeeds()
        carbs_l = float("{0:.2f}".format(carbs[0]))
        carbs_u = float("{0:.2f}".format(carbs[1]))
        print("Carbs : lower limit %f , upper limit %f" % (carbs[0], carbs[1]))
        fats = nutrition.calculateFasNeeds()
        print("fats :  %f" % fats)
        #Session["Calories"] = cal
        return render_template('Main.html',cal=cal,pro_l=pro_l,pro_u=pro_u,carbs_u=carbs_u,carbs_l=carbs_l,fats=fats)
@app.route('/getNutrition', methods=['POST'])
def getNutrtion():
    print('inside get nutrition')
    if request.method=='POST':
        print('mlmlmlmlmlmlmlmlml')
        useritem = request.form.get('itemName')
        print(useritem)
        itemStr = request.form.get('itemStr')
        print(itemStr)
        if(useritem ):
            print("inside if")
            nutritionValList = getNutritionfacts(useritem)
            return render_template('Main.html', calIntake=nutritionValList[0], proIntake=nutritionValList[1],
                                   carbsIntake=nutritionValList[2], fatsIntake=nutritionValList[3], useritem=useritem,
                                   qty=nutritionValList[4], servingUnit=nutritionValList[5])


        elif(itemStr):
            print("inside elif")
            print(itemStr)
            nutritionValdict = getNutritionfactsForPlainText(itemStr)
            print(nutritionValdict)
            #return render_template('Main.html',calIntake=nutritionValList[0],proIntake=nutritionValList[1],carbsIntake=nutritionValList[2],fatsIntake=nutritionValList[3],useritem=useritem,qty=nutritionValList[4],servingUnit=nutritionValList[5])
            return render_template('Main.html',nutritionValdict=nutritionValdict)
@app.route('/getItemName', methods=['POST','GET'])
def getNutritionforAutocomplete():
    print('mlmlmlmlmlmlmlmlml')
    useritem = request.form.get('itemName')
    itemList = getNutritionfactswithAutocomplete(useritem)
    return render_template("enterLunch.html",itemList=itemList)


if __name__ == '__main__':
    app.debug = True
    app.debug = True
    app.run()




