import json
import time
import datetime
from requests import put, get , post

if __name__ == '__main__':
    url = "https://trackapi.nutritionix.com/v2/search/instant?query=milk"
    url2="https://trackapi.nutritionix.com/v2/natural/nutrients"
    content_type_header = "application/json"
    APPID = "3e521ea4"
    APPKEY = "84891aa0b5c69afcc9292eec166b6ae6"
    headers = {'Content-Type': content_type_header,'x-app-id': APPID ,'x-app-key':APPKEY}
    r = get(url,headers=headers).json()
    for  item in r:
        if(item=="common"):
            itemName = r[item][0]["food_name"]
            items = {"query": itemName,"timezone": "US/Eastern"}
            r2 = post(url2,data=json.dumps(items),headers=headers).json()
            print( r2['foods'][0])
            if(r2['foods'][0]["food_name"]==itemName):
                if(r2['foods'][0]["serving_qty"]==1):
                    print(r2["foods"][0]["nf_calories"])
                    print(r2['foods'][0]["nf_total_fat"])
                    print(r2['foods'][0]["nf_sugars"])
                    print(r2['foods'][0]["nf_protein"])
                    print(r2['foods'][0]["nf_total_carbohydrate"])







