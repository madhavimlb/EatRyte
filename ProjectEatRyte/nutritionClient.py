from requests import put, get
from nutritionix import Nutritionix

nix = Nutritionix(app_id="3e521ea4", api_key="84891aa0b5c69afcc9292eec166b6ae6")
pizza = nix.search("pizza")
print (pizza)
results = pizza.json()
print (results)