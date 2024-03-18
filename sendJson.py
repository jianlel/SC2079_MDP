import requests 
import json  
url = "http://127.0.0.1:5000" 
 
 
#filename = r'C:\Users\hooji\OneDrive\Desktop\holder\json.txt'

x = {
  "cat": "obstacles",
  "value": {
    "obstacles": [
      {
        "x": 7,
        "y": 10,
        "d": 4,
        "id": 1
      },
      {
        "x": 7,
        "y": 14,
        "d": 6,
        "id": 2
      },
      {
        "x": 12,
        "y": 9,
        "d": 2,
        "id": 3
      },

    ],
    "mode": "0"
  }
}	

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
