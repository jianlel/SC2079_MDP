import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *
import os
from ultralytics import YOLO
app = Flask(__name__)
CORS(app)
#model = load_model()
model = YOLO('last.pt')
@app.route('/status', methods=['GET'])
def status():
    """
    This is a health check endpoint to check if the server is running
    :return: a json object with a key "result" and value "ok"
    """
    return jsonify({"result": "ok"})

@app.route('/image', methods=['POST'])
def image_predict():
    """
    This is the main endpoint for the image prediction algorithm
    :return: a json object with a key "result" and value a dictionary with keys "obstacle_id" and "image_id"
    """
    file = request.files['file']
    #filename = f"C:\\Use{count}.jpg"
    #filename = file.filename
    #print(filename)
    # filename_v2 = '\\'.join(os.path.dirname(filename).split("/"))
    # corrected_path = filename_v2.replace("\\", "\\\\")
    # print(corrected_path)
    file.save(f'C:\\Users\\sanja\\OneDrive\\Desktop\\rpi_upload\\img_{int(time.time())}.jpeg')  # filename format: "<timestamp>_<obstacle_id>_<signal>.jpeg"
    filename = f"C:\\Users\\sanja\\OneDrive\\Desktop\\rpi_upload\\img_{int(time.time())}.jpeg"
    constituents = file.filename.split("_")
    # obstacle_id = constituents[1]
    # signal = constituents[2].strip(".jpg")

    # Week 8 ## 
    signal = constituents[2].strip(".jpg")
    image_id = predict_image_week_9(filename, model, signal)

    # ## Week 9 ## 
    # # We don't need to pass in the signal anymore
    # filename = f"C:\\Users\\sanja\\OneDrive\\Desktop\\rpi_upload\\img_{int(time.time())}.jpg"
    # print(signal)
    # Return the obstacle_id and image_id
    result = {
        "image_id": image_id,
        #"obstacle_id": obstacle_id	
    }
    return jsonify(result)

@app.route('/stitch', methods=['GET'])
def stitch():
    """
    This is the main endpoint for the stitching command. Stitches the images using two different functions, in effect creating two stitches, just for redundancy purposes
    """
    img = stitch_image()
    img.show()
    #img2 = stitch_image_own()
    #img2.show()
    #return jsonify({"result": "ok"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
