from flask import Flask, request
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
        
        # Process each obstacle
        for obstacle_key, obstacle_value in json_data.items():
            x = obstacle_value.get("x")
            y = obstacle_value.get("y")
            direction = obstacle_value.get("direction")
            uid = obstacle_value.get("uid")
            
            # Process the obstacle data as needed
            print(f"Obstacle {obstacle_key}: (x={x}, y={y}), direction={direction}, uid={uid}")
        
        return 'JSON received and processed successfully'
    
    except json.JSONDecodeError as e:
        return f'Error decoding JSON: {e}', 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)