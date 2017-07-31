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
global userid

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
    conn = mysql.get_db()
    cur = conn.cursor()
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
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO  `RequiredNutrition` (`userId`,`cal`,`pro_l`,`pro_u`,`carbs_l`,`carbs_u`,`fats`) VALUES (1001,%s,%s,%s,%s,%s,%s );",(cal, pro_l, pro_u,carbs_l,carbs_u, fats))
        data_nutriInfo = cur.fetchall()
        conn.commit()

        return render_template('Main.html',cal=cal,pro_l=pro_l,pro_u=pro_u,carbs_u=carbs_u,carbs_l=carbs_l,fats=fats)
@app.route('/getNutrition', methods=['POST'])
def getNutrtion():
    print('inside get nutrition')
    if request.method=='POST':
        useritem = request.form.get('itemName')
        print(useritem)
        itemStr = request.form.get('itemStr')
        print(itemStr)
        today =time.strftime('%Y-%m-%d')
        conn = mysql.get_db()
        cur = conn.cursor()


        if(useritem ):
            quant = request.form.get('quantity')
            quan = quant.split();
            quantity = float(quan[0])
            servingUnit = quan[1]
            foodIntakelist_current = ["Breakfast", useritem, quantity, servingUnit]
            print(quan)
            cur.execute("INSERT INTO  `Mealinfo` (`type`,`item`,`quantity`,`servingUnit`,`userId`,`date`) VALUES ('Breakfast',%s,%s,%s,%s,%s );",(useritem, quantity, servingUnit, 1001, today))
            #cur.execute("SELECT `item` , `quantity`,`servingUnit` FROM `Mealinfo` WHERE userId=1001")
            data = cur.fetchall()
            conn.commit()
            useremaildb = cur.fetchone()
            print(type(data))
            print("--------------------@@@@@@@@@@@@@")
            print(data)
            print("inside if")
            nutritionValList = getNutritionfacts(useritem,quant)
            calIntake=nutritionValList[0]
            proIntake = nutritionValList[1]
            carbsIntake = nutritionValList[2]
            fatsIntake = nutritionValList[3]
            cur.execute("SELECT `calories`,`fats`,`carbohydrates`,`protien`,`date` FROM `NutritionInfo` WHERE `userId`=1001 and `date` ="+today)
            data_nutriInfo = cur.fetchall()
            print("dat nutri info !!!!!")
            print(data_nutriInfo)
            print(len(data_nutriInfo))
            print("----------inside else !!!!!  ")
            cur.execute("INSERT INTO  `NutritionInfo` (`userId`,`type`,`calories`,`fats`,`carbohydrates`,`protien`,`date`) VALUES (1001,'Breakfast',%s,%s,%s,%s,%s );",(calIntake,fatsIntake,carbsIntake,proIntake,today))
            data = cur.fetchall()
            conn.commit()
            return render_template('Main.html', calIntake=nutritionValList[0], proIntake=nutritionValList[1],
                                   carbsIntake=nutritionValList[2], fatsIntake=nutritionValList[3], useritem=useritem,
                                   qty=nutritionValList[4], servingUnit=nutritionValList[5],data=data)


        elif(itemStr):
            print("inside elif")
            print(itemStr)
            nutritionValdict = getNutritionfactsForPlainText(itemStr)
            for key in nutritionValdict:
                item=key
                quan = nutritionValdict[key][4]
                servingUnit = nutritionValdict[key][5]
                cur.execute("INSERT INTO  `Mealinfo` (`type`,`item`,`quantity`,`servingUnit`,`userId`,`date`) VALUES ('Breakfast',%s,%s,%s,%s,%s );",
                    (item, quan, servingUnit, 1001, today))
            cur.execute("SELECT `item` , `quantity`,`servingUnit` FROM `Mealinfo` WHERE userId=1001")
            data = cur.fetchall()
            conn.commit()
            print(nutritionValdict)
            #return render_template('Main.html',calIntake=nutritionValList[0],proIntake=nutritionValList[1],carbsIntake=nutritionValList[2],fatsIntake=nutritionValList[3],useritem=useritem,qty=nutritionValList[4],servingUnit=nutritionValList[5])
            return render_template('Main.html',nutritionValdict=nutritionValdict,dataFromspecificMeal=data)
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




