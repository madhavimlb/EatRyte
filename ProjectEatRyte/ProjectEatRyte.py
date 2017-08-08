from flask import Flask, render_template, request
from NutritionReqCalculatorForm import *
from flask import flash
from nutritionAPI import *
from flask_wtf.csrf import CSRFProtect
from calculateActualNutrition import *
from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL
from datetime import datetime
import datetime as dt

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


@app.route('/mydashboard')
def chart():
    conn = mysql.get_db()
    cur = conn.cursor()
    today = time.strftime('%Y-%m-%d')
    print(type(today))
    print("@@@@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@@@!!!!!!!!!!!!!!!")
    query = "SELECT calories, fats, carbohydrates, protien, `date` FROM NutritionInfo WHERE userid='1001' and date='" + today + "'"
    cur.execute(query)
    # cur.execute("SELECT `calories`,`fats`,`carbohydrates`,`protien`,`date` FROM `NutritionInfo` WHERE `userId`=1001 AND `date`="+'today')
    data_nutriInfo = cur.fetchall()
    conn.commit()
    query_reqNutrition = "SELECT cal, fats, pro_l,carbs_l FROM RequiredNutrition WHERE userid='1001'"
    cur.execute(query_reqNutrition)
    data_reqNutriInfo = cur.fetchall()
    print("@@@@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@@@")
    print(data_nutriInfo)
    conn.commit()
    total_cal = 0
    total_fats = 0
    total_pro = 0
    total_carbs = 0
    req_cal = 0
    req_fats = 0
    req_pro = 0
    req_carbs = 0
    for each in data_nutriInfo:
        total_cal = total_cal + float(each[0])
        total_fats = total_fats + float(each[1])
        total_pro = total_pro + float(each[2])
        total_carbs = total_carbs + float(each[3])

    for each in data_reqNutriInfo:
        req_cal = float(each[0])
        req_fats = float(each[1])
        req_pro = float(each[2])
        req_carbs = float(each[3])

    return render_template('displaygraph.html', reqCal=json.dumps(req_cal), total_cal=json.dumps(total_cal),
                           req_fats=json.dumps(req_fats), total_fats=json.dumps(total_fats),
                           req_pro=json.dumps(req_pro), total_pro=json.dumps(total_pro),
                           total_carbs=json.dumps(total_carbs), req_carbs=json.dumps(req_carbs))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    conn = mysql.get_db()
    cur = mysql.connect().cursor()
    today = time.strftime('%Y-%m-%d')
    cur.execute('SELECT email FROM EatRyte.users')
    useremaildb = cur.fetchone()
    cur.execute('SELECT pwdhash FROM EatRyte.users')
    userpwdb = cur.fetchone()
    cur.execute('SELECT uid FROM EatRyte.users')
    userid = cur.fetchone()
    cur.execute('SELECT firstname FROM EatRyte.users')
    fname = cur.fetchone()
    print("login login login")
    print('email')
    print(useremaildb)
    print(userpwdb)
    print(type(fname))

    if request.method == 'POST':
        print("inside ")
        print(type(useremaildb[0]))
        print(useremaildb[0])
        print(userpwdb[0])
        print(type(request.form.get('email')))
        print(request.form.get('email'))
        print(request.form.get('password'))
        cal = 0
        pro_l = 0
        pro_u = 0
        carbs_l = 0
        carbs_u = 0
        fats = 0
        if str(request.form.get('email')) == str(useremaildb[0]) and  str(request.form.get('password')) == str(userpwdb[0]) :
            print("inside if ")
            username=fname[0]
            print("Printing fname :    " + username)
            print(type(userid[0]))

            cur.execute("SELECT `cal`,`pro_l`,`pro_u`,`carbs_l`,`carbs_u`,`fats` FROM `RequiredNutrition` WHERE `userId`= "+ str(userid[0]))
            data_nutriInfo = cur.fetchone()
            print("----------------data_nutriInfo------------------")
            print(type(data_nutriInfo))

            if data_nutriInfo is not None:
                print("----------------data_nutriInfo  inside if ------------------")
                cal=  data_nutriInfo[0]
                pro_l = data_nutriInfo[1]
                pro_u = data_nutriInfo[2]
                carbs_l = data_nutriInfo[3]
                carbs_u = data_nutriInfo[4]
                fats = data_nutriInfo[4]
                print("----------------login------------------")
                print(data_nutriInfo)
                conn.commit()
            cur.execute(
                    "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Breakfast' and date='" + today + "'")
            data_fromMealInfo_Breakfast = cur.fetchall()
            conn.commit()
            cur.execute(
                    "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Lunch' and date='" + today + "'")
            data_fromMealInfo_Lunch = cur.fetchall()
            conn.commit()
            cur.execute(
                    "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Dinner' and date='" + today + "'")
            data_fromMealInfo_Dinner = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Others' and date='" + today + "'")
            data_fromMealInfo_Others = cur.fetchall()
            conn.commit()

            #return render_template('main.html')
            return render_template('main.html', username=username,cal=cal, pro_l=pro_l, pro_u=pro_u, carbs_u=carbs_u, carbs_l=carbs_l,
                              fats=fats,data_fromMealInfo_Breakfast=data_fromMealInfo_Breakfast,data_fromMealInfo_Lunch=data_fromMealInfo_Lunch,data_fromMealInfo_Dinner=data_fromMealInfo_Dinner, data_fromMealInfo_Others=data_fromMealInfo_Others)



@app.route('/enterNutriDetails', methods=['POST'])
def enterNutritionDetails():
    print('okokokokoko')
    conn = mysql.get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        index = 1
        sex = request.form.get('sex')
        print(sex)
        weight = request.form.get('weight')
        print(weight)
        height = request.form.get('height')
        print(height)
        age = request.form.get('age')
        print(age)
        physicalActivity = request.form.get('physical activity')
        print(physicalActivity)
        nutrition = actualNutrition(sex, height, weight, age, physicalActivity)
        cal = nutrition.calulateCalorieNeeds()
        cal = float("{0:.2f}".format(cal))
        print("------------------tyoe cal ---------------------")
        print(type(cal))
        print("Calories : %f" % cal)
        pro = nutrition.calulateProteinNeeds()
        pro_l = float("{0:.2f}".format(pro[0]))
        pro_u = float("{0:.2f}".format(pro[1]))
        print("Protiens : lower limit %f , upper limit %f" % (pro[0], pro[1]))
        carbs = nutrition.calculateCarbsNeeds()
        carbs_l = float("{0:.2f}".format(carbs[0]))
        carbs_u = float("{0:.2f}".format(carbs[1]))
        print("Carbs : lower limit %f , upper limit %f" % (carbs[0], carbs[1]))
        fats = nutrition.calculateFasNeeds()
        print("fats :  %f" % fats)
        # Session["Calories"] = cal
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO  `RequiredNutrition` (`userId`,`cal`,`pro_l`,`pro_u`,`carbs_l`,`carbs_u`,`fats`) VALUES (1001,%s,%s,%s,%s,%s,%s );",
            (cal, pro_l, pro_u, carbs_l, carbs_u, fats))
        data_nutriInfo = cur.fetchall()
        conn.commit()

        return render_template('Main.html', cal=cal, pro_l=pro_l, pro_u=pro_u, carbs_u=carbs_u, carbs_l=carbs_l,
                               fats=fats)

@app.route('/getNutrition', methods=['POST'])
def getNutrtion():
    print('inside get nutrition')
    if request.method == 'POST':
        useritem = request.form.get('itemName')
        print(useritem)
        itemStr = request.form.get('itemStr')
        print(itemStr)
        mealType = request.form.get('mealType')
        print("-----------------------------------------mealtype")
        print(mealType)
        today = time.strftime('%Y-%m-%d')
        conn = mysql.get_db()
        cur = conn.cursor()

        if (useritem):
            quant = request.form.get('quantity')
            quan = quant.split();
            quantity = float(quan[0])
            servingUnit = quan[1]
            foodIntakelist_current = ["Breakfast", useritem, quantity, servingUnit]
            print(quan)
            cur.execute(
                "INSERT INTO  `Mealinfo` (`type`,`item`,`quantity`,`servingUnit`,`userId`,`date`) VALUES (%s,%s,%s,%s,%s,%s );",
                (mealType, useritem, quantity, servingUnit, 1001, today))
            # cur.execute("SELECT `item` , `quantity`,`servingUnit` FROM `Mealinfo` WHERE userId=1001")
            data = cur.fetchall()
            conn.commit()
            useremaildb = cur.fetchone()
            print(type(data))
            print("--------------------@@@@@@@@@@@@@")
            print(data)
            print("inside if")
            nutritionValList = getNutritionfacts(useritem, quant)
            calIntake = nutritionValList[0]
            proIntake = nutritionValList[1]
            carbsIntake = nutritionValList[2]
            fatsIntake = nutritionValList[3]
            cur.execute(
                "SELECT `calories`,`fats`,`carbohydrates`,`protien`,`date` FROM `NutritionInfo` WHERE `userId`=1001 and date='" + today + "'")
            data_nutriInfo = cur.fetchall()
            print("dat nutri info !!!!!")
            print(data_nutriInfo)
            print(len(data_nutriInfo))
            print("----------inside else !!!!!  ")
            cur.execute(
                "INSERT INTO  `NutritionInfo` (`userId`,`type`,`calories`,`fats`,`carbohydrates`,`protien`,`date`) VALUES (1001,%s,%s,%s,%s,%s,%s );",
                (mealType, calIntake, fatsIntake, carbsIntake, proIntake, today))
            data = cur.fetchall()
            print("printingggggggg dataaaa")
            print(data)
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Breakfast' and date='" + today + "'")
            data_fromMealInfo_Breakfast = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Lunch' and date='" + today + "'")
            data_fromMealInfo_Lunch = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Dinner' and date='" + today + "'")
            data_fromMealInfo_Dinner = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Others' and date='" + today + "'")
            data_fromMealInfo_Others = cur.fetchall()
            conn.commit()
            print(data_fromMealInfo_Breakfast)
            print(data_fromMealInfo_Lunch)
            print(data_fromMealInfo_Dinner)
            print(data_fromMealInfo_Others)
            print("last linnnnnnnnnnnn print data")
            return render_template('Main.html', calIntake=nutritionValList[0], proIntake=nutritionValList[1],
                                   carbsIntake=nutritionValList[2], fatsIntake=nutritionValList[3], useritem=useritem,
                                   qty=nutritionValList[4], servingUnit=nutritionValList[5],
                                   data_fromMealInfo_Breakfast=data_fromMealInfo_Breakfast,data_fromMealInfo_Lunch=data_fromMealInfo_Lunch,data_fromMealInfo_Dinner=data_fromMealInfo_Dinner,data_fromMealInfo_Others=data_fromMealInfo_Others)


        elif (itemStr):
            print("inside elif")
            print(itemStr)
            nutritionValdict = getNutritionfactsForPlainText(itemStr)
            print("oooooooooooo")
            print(nutritionValdict)
            for key in nutritionValdict:
                item = key
                quan = nutritionValdict[key][4]
                servingUnit = nutritionValdict[key][5]

                calIntake = nutritionValdict[key][0]
                proIntake = nutritionValdict[key][1]
                carbsIntake = nutritionValdict[key][2]
                fatsIntake = nutritionValdict[key][3]
                cur.execute(
                    "INSERT INTO  `Mealinfo` (`type`,`item`,`quantity`,`servingUnit`,`userId`,`date`) VALUES (%s,%s,%s,%s,%s,%s );",
                    (mealType,item, quan, servingUnit, 1001, today))
                conn.commit()
                cur.execute(
                    "INSERT INTO  `NutritionInfo` (`userId`,`type`,`calories`,`fats`,`carbohydrates`,`protien`,`date`) VALUES (1001,%s,%s,%s,%s,%s,%s );",
                    (mealType, calIntake, fatsIntake, carbsIntake, proIntake, today))
                data = cur.fetchall()
                print("printingggggggg dataaaa")
                print(data)
                conn.commit()
            cur.execute(
                "SELECT `item` , `quantity`,`servingUnit` FROM `Mealinfo` WHERE userId=1001 and date='" + today + "'")
            data = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Breakfast' and date='" + today + "'")
            dataFromspecificMeal_Breakfast = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Lunch' and date='" + today + "'")
            dataFromspecificMeal_Lunch = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Dinner' and date='" + today + "'")
            dataFromspecificMeal_Dinner = cur.fetchall()
            conn.commit()
            cur.execute(
                "SELECT `item`,`quantity`,`servingUnit` FROM `Mealinfo` WHERE `userId`=1001 and `type` = 'Others' and date='" + today + "'")
            dataFromspecificMeal_Others = cur.fetchall()
            conn.commit()
            print(nutritionValdict)
            # return render_template('Main.html',calIntake=nutritionValList[0],proIntake=nutritionValList[1],carbsIntake=nutritionValList[2],fatsIntake=nutritionValList[3],useritem=useritem,qty=nutritionValList[4],servingUnit=nutritionValList[5])
            return render_template('Main.html', nutritionValdict=nutritionValdict, dataFromspecificMeal_Breakfast=dataFromspecificMeal_Breakfast,dataFromspecificMeal_Lunch=dataFromspecificMeal_Lunch,dataFromspecificMeal_Dinner=dataFromspecificMeal_Dinner,dataFromspecificMeal_Others=dataFromspecificMeal_Others)


@app.route('/getItemName', methods=['POST', 'GET'])
def getNutritionforAutocomplete():
    print('mlmlmlmlmlmlmlmlml')
    useritem = request.form.get('itemName')
    itemList = getNutritionfactswithAutocomplete(useritem)
    return render_template("enterLunch.html", itemList=itemList)


if __name__ == '__main__':
    app.debug = True
    app.debug = True
    app.run()
