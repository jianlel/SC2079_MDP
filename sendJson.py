import requests 
import json  
url = "http://127.0.0.1:5000" 
 
 
filename = r'C:\Users\hooji\OneDrive\Desktop\holder\json.txt'

x = {
	"obstacle1": {"x": 70, "y": 100, "direction": "s", "uid": 1},
	"obstacle2": {"x": 70, "y": 140, "direction": "w", "uid": 2},
	"obstacle3": {"x": 120, "y": 90, "direction": "e", "uid": 3},
	"obstacle4": {"x": 150, "y": 150, "direction": "s", "uid": 4},
	"obstacle5": {"x": 150, "y": 40, "direction": "w", "uid": 5}
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
