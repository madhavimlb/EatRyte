from flask import Flask, render_template,request
from NutritionReqCalculatorForm import *
from flask import flash
from nutritionAPI import *
from flask_wtf.csrf import CSRFProtect
from calculateActualNutrition import *
from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL
import time

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'EatRyte'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
global username
global  userid

@app.route('/')
def homepage():
    print('inside static page')
    return render_template('index.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    cur = mysql.connect().cursor()
    cur.execute('SELECT email FROM EatRyte.users')
    useremaildb = cur.fetchone()
    cur.execute('SELECT pwdhash FROM EatRyte.users')
    userpwdb = cur.fetchone()
    cur.execute('SELECT uid FROM EatRyte.users')
    userid = cur.fetchone()
    print('email' )
    print(useremaildb)
    print( userpwdb)


    if request.method == 'POST':
        if request.form['email'] != useremaildb or request.form['password'] != 'userpwdb':
            error = 'Invalid Credentials. Please try again.'
            print(error)
        else:
            return redirect(url_for('home'))
    return render_template('main.html', error=error)


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
        quant = request.form.get('quantity')
        quan =float(quant.split());
        quantity = quan[0]
        servingUnit = quan[1]
        foodIntakelist=["Breakfast",useritem,quantity,servingUnit]
        print(quan)
        itemStr = request.form.get('itemStr')
        print(itemStr)
        time.strftime("%H:%M:%S")
        cur = mysql.connect().cursor()
        cur.execute("INSERT INTO EatRyte.Meal ('type','item','quantity','servingUnit','userId','date') VALUES ('Breakfast', useritem, quantity,servingUnit,userid,);")
        useremaildb = cur.fetchone()
        if(useritem ):
            print("inside if")
            nutritionValList = getNutritionfacts(useritem,quant)
            return render_template('Main.html', calIntake=nutritionValList[0], proIntake=nutritionValList[1],
                                   carbsIntake=nutritionValList[2], fatsIntake=nutritionValList[3], useritem=useritem,
                                   qty=nutritionValList[4], servingUnit=nutritionValList[5],foodIntakelist=foodIntakelist)


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




