import requests 
import json  
url = "http://127.0.0.1:5000" 
 
 
#filename = r'C:\Users\hooji\OneDrive\Desktop\holder\json.txt'

x = {'cat': 'obstacles', 'value': {'obstacles': [{'x': 2, 'y': 12, 'd': 0, 'id': 0}, {'x': 8, 'y': 0, 'd': 0, 'id': 0}, {'x': 18, 'y': 2, 'd': 0, 'id': 0}, {'x': 2, 'y': 11, 'd': 4, 'id': 0}, {'x': 6, 'y': 10, 'd': 2, 'id': 0}, {'x': 15, 'y': 9, 'd': 4, 'id': 0}, {'x': 19, 'y': 15, 'd': 0, 'id': 0}, {'x': 11, 'y': 18, 'd': 4, 'id': 0}], 'mode': '0'}}

#json_converted = json.dumps(x, indent = 4)	
#print(type(json_converted))
#print(json_converted)

#response = requests.post(url, files={"file": (filename, open(filename,'rb'))})
response = requests.post(url, json = x) 

if response.status_code != 200: 
    print("Something went wrong when requesting path from the Algo server. Please try again.") 
 
print("Response status: ", response.status_code)
print("Response text: ", response.text)


#response_json = json.dumps(response)
#parsed_response = json.loads(response_json)
#print(parsed_response)
