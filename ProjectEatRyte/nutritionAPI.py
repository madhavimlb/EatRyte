
import datetime
from requests import put, get , post
import requests, json

#if __name__ == '__main__':
def getNutritionfacts_old(useritem,userBrand,userquantity,usermealtype):
    print('inside get nutri facts')
    url = "https://trackapi.nutritionix.com/v2/search/instant?query="+useritem
    url2="https://trackapi.nutritionix.com/v2/natural/nutrients"
    content_type_header = "application/json"
    APPID = "3e521ea4"
    APPKEY = "5d77a59b4d71536cc2d42aaaa8b36c22"
    headers = {'Content-Type': content_type_header,'x-app-id': APPID ,'x-app-key':APPKEY}
    r = get(url,headers=headers).json()
    print(usermealtype)
    print(r)
    for item in r:
        #print(item)
       if(usermealtype=="common"):
            itemName = r[item][0]["food_name"]

            items = {"query": itemName,"timezone": "US/Eastern"}
            r2 = post(url2,data=json.dumps(items),headers=headers).json()
            print (r2)
            if(r2['foods'][0]["food_name"]==itemName):
                    print("-------------------------------------------------")
                    qty = r2['foods'][0]["serving_qty"]
                    servingUnit =r2['foods'][0]["serving_unit"]
                    print(r2['foods'][0]["serving_qty"])
                    print("Calories")
                    print(r2["foods"][0]["nf_calories"])
                    cal =  r2["foods"][0]["nf_calories"]
                    print("Fat")
                    print(r2['foods'][0]["nf_total_fat"])
                    fat =  r2['foods'][0]["nf_total_fat"]
                    print("Sugars")
                    print(r2['foods'][0]["nf_sugars"])
                    print("Protein")
                    print(r2['foods'][0]["nf_protein"])
                    pro = r2['foods'][0]["nf_protein"]
                    print("Carbohydrates")
                    print(r2['foods'][0]["nf_total_carbohydrate"])
                    carb= r2['foods'][0]["nf_total_carbohydrate"]
                    return [cal,pro,carb,fat,qty,servingUnit]
       elif(usermealtype=="branded"):
            print("branded")
            itemName = r[item][0]["food_name"]
            print("itemName"+itemName)
            items = {"query": itemName, "timezone": "US/Eastern"}
            r2 = post(url2, data=json.dumps(items), headers=headers).json()
            print(r2)
            print("branded nix is ")
            print("Calories")
            print(r2["foods"][0]["nf_calories"])
            print("Fat")
            print(r2['foods'][0]["nf_total_fat"])
            print("Sugars")
            print(r2['foods'][0]["nf_sugars"])
            print("Protein")
            print(r2['foods'][0]["nf_protein"])
            print("Carbohydrates")
            print(r2['foods'][0]["nf_total_carbohydrate"])



def getNutritionfacts(userItem,quant):
        content_type_header = "application/json"
        APPID = "3e521ea4"
        APPKEY = "5d77a59b4d71536cc2d42aaaa8b36c22"
        formdata = {"query":userItem,"timezone": "US/Eastern"}
        url2= "https://trackapi.nutritionix.com/v2/natural/nutrients/"
        headers= {'Content-Type': content_type_header, 'X-APP-ID': APPID, 'X-APP-KEY': APPKEY}
        response = requests.post(url2, headers=headers,data=json.dumps(formdata))
        print("outside if in get getNutritionfacts()")
        quan=quant.split()
        print("--------------type- quantity -----------")

        quantity = float(quan[0])
        print(type(quantity))
        errorMsg='Please enter valid serving unip'

        r2 = json.loads(response.text)
        print(r2)
        for each in r2:

            print(type(r2['foods'][0]['food_name']))
            print(type(userItem))
            if (str.lower(r2['foods'][0]['food_name'])== str.lower(userItem)):

                print("--------------------ppppppppp-----------------------------")
                qty = r2['foods'][0]["serving_qty"]
                servingUnit = r2['foods'][0]["serving_unit"]
               # if(servingUnit==quan[1]):
                print(r2['foods'][0]["serving_qty"])
                print("Calories")
                print(r2["foods"][0]["nf_calories"])
                cal = (r2["foods"][0]["nf_calories"] )

                print(type(cal))
                cal = cal * quantity
                print(type(cal))
                print("Fat")
                print(r2['foods'][0]["nf_total_fat"])
                fat = (r2['foods'][0]["nf_total_fat"]) *quantity
                print("Sugars")
                print(r2['foods'][0]["nf_sugars"])
                print("Protein")
                print(r2['foods'][0]["nf_protein"])
                pro = (r2['foods'][0]["nf_protein"]) * quantity
                print("Carbohydrates")
                print(r2['foods'][0]["nf_total_carbohydrate"])
                carb = (r2['foods'][0]["nf_total_carbohydrate"]) * quantity
                #else:
                    #return errorMsg
            return [cal, pro, carb, fat, qty, servingUnit]


def getNutritionfactsForPlainText(userItem):
    content_type_header = "application/json"
    APPID = "3e521ea4"
    APPKEY = "5d77a59b4d71536cc2d42aaaa8b36c22"
    formdata = {"query": userItem, "timezone": "US/Eastern"}
    url2 = "https://trackapi.nutritionix.com/v2/natural/nutrients/"
    headers = {'Content-Type': content_type_header, 'X-APP-ID': APPID, 'X-APP-KEY': APPKEY}
    response = requests.post(url2, headers=headers, data=json.dumps(formdata))
    print("outside if in get getNutritionfacts()")
    r2 = json.loads(response.text)
    print(r2)
    dict={}
    for each in r2['foods']:
            print("printing each")
            print(each)
            print("inside correct for")
            print(each['food_name'])
            #print(userItem)

            print("-------------------------------------------------")
            qty = each["serving_qty"]
            servingUnit = each["serving_unit"]
            print(each["serving_qty"])
            print("Calories")
            print(each["nf_calories"])
            cal = each["nf_calories"]
            print("Fat")
            print(each["nf_total_fat"])
            fat = each["nf_total_fat"]
            print("Sugars")
            print(each["nf_sugars"])
            print("Protein")
            print(each["nf_protein"])
            pro = each["nf_protein"]
            print("Carbohydrates")
            print(each["nf_total_carbohydrate"])
            carb = each["nf_total_carbohydrate"]
            print("blahblahblah")
            dict[each['food_name']]=[cal, pro, carb, fat, qty, servingUnit]
    return dict
#if __name__ == '__main__':
def getNutritionfactswithAutocomplete(useritem):
        print("---------------")
        url =  "https://api.nutritionix.com/v2/autocomplete?q="+useritem
        #content_type_header = "application/json"
        APPID = "3e521ea4"
        APPKEY = "5d77a59b4d71536cc2d42aaaa8b36c22"
        # = {'Content-Type': content_type_header, 'X-APP-ID': APPID, 'X-APP-KEY': APPKEY}
        headers = {'X-APP-ID': APPID, 'X-APP-KEY': APPKEY}
        r = get(url,headers=headers).json()
        print(r)
        itemList=[]
        for item in r:
            print(item['text'])
            itemName = item['text']
            itemList.append(itemName)
        return itemList


