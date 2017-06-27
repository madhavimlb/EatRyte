import json
import time
import datetime
from requests import put, get , post

#if __name__ == '__main__':
def getNutritionfacts(useritem ,userBrand, userquantity,usermealtype):
    print('inside get nutri facts')
    url = "https://trackapi.nutritionix.com/v2/search/instant?query="+useritem
    url2="https://trackapi.nutritionix.com/v2/natural/nutrients"
    content_type_header = "application/json"
    APPID = "3e521ea4"
    APPKEY = "5d77a59b4d71536cc2d42aaaa8b36c22"
    headers = {'Content-Type': content_type_header,'x-app-id': APPID ,'x-app-key':APPKEY}
    r = get(url,headers=headers).json()
    print(usermealtype)
    #print(r)
    for  item in r:
        #print(item)
        if(usermealtype=="common"):
            itemName = r[item][0]["food_name"]
            items = {"query": itemName,"timezone": "US/Eastern"}
            r2 = post(url2,data=json.dumps(items),headers=headers).json()
            print( r2['foods'][0])
            if(r2['foods'][0]["food_name"]==itemName):
                    print("-------------------------------------------------")
                    print(r2['foods'][0]["serving_qty"])
                    print(r2["foods"][0]["nf_calories"])
                    print(r2['foods'][0]["nf_total_fat"])
                    print(r2['foods'][0]["nf_sugars"])
                    print(r2['foods'][0]["nf_protein"])
                    print(r2['foods'][0]["nf_total_carbohydrate"])
        elif(usermealtype=="branded"):
            print("branded")
            itemName = r[item][0]["food_name"]
            print("itemName"+itemName)
            items = {"query": itemName, "timezone": "US/Eastern"}
            r2 = post(url2, data=json.dumps(items), headers=headers).json()
            print(r2)
            print("branded nix is ")
            print(r2["foods"][0]["nf_calories"])
            print(r2['foods'][0]["nf_total_fat"])
            print(r2['foods'][0]["nf_sugars"])
            print(r2['foods'][0]["nf_protein"])
            print(r2['foods'][0]["nf_total_carbohydrate"])






