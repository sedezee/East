import json 
import requests

with open ("data_storage.json", "r") as file: 
    data = json.load(file)


  

print(data[0]["admin_id"])
