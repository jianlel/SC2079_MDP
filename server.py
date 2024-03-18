from flask import Flask, request
import Helper.settings as settings
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_json():
    # If receiving from a file
    #if 'file' not in request.files:
    #    return 'No file in the request', 400
    
    #file = request.files['file']

    #json_data = file.read()
    #json_data = request.json()

    try:
        # Decode the JSON data
        json_data = request.json
        #obstacles_data = json.loads(json_data)

        # Extract obstacle values
        obstacles = json_data["value"]["obstacles"]

        # Access individual obstacle values
        for obstacle in obstacles:
            x = obstacle["x"]
            y = obstacle["y"]
            id = obstacle["id"]
            dir_code = obstacle["d"]
            dir = settings.DIR[int(dir_code)]  # Map direction code to direction
            print(f"x = {x}, y = {y}, id = {id}, dir = {dir}")
            
        return 'JSON received and processed successfully'
        
    except json.JSONDecodeError as e:
        return f'Error decoding JSON: {e}', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
