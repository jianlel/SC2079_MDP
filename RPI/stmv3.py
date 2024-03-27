import time
import json
import picamera
import requests
import io
import os
img_no = 0

def capture_image():
    global img_no
    with open("/home/pi/Desktop/obs_ids.txt", "r") as f:
        contents = f.read()
        obs_ids = contents.split("\n")

    with open("/home/pi/Desktop/detection.txt", "r") as file:
        content = file.read()
        detection_side = content.split("\n")

    with picamera.PiCamera() as camera:
        camera.resolution = (512, 256)
        timez = int(time.time())
        photo_path = f("/home/pi/Desktop/rpi_uploads/{timez}_{obs_ids[img_no]}_{detection_side[img_no]}.jpg")
        filename = f"{timez}_{obs_ids[img_no]}_{detection_side[img_no]}.jpg"
        img_no += 1
        #print(filename)
        camera.capture(photo_path, format="jpeg", quality = 25)

        return filename
    
def send_image_for_recognition(filename):
    url = "http://192.168.15.13:5000/image"
    filename = "/home/pi/Desktop/rpi_uploads/" + filename

    with open(filename, 'rb') as file:
        response = requests.post(url, files = {"file": (os.path.basename(filename), file)})
    #print(f"img rec result is {response})
    results = json.loads(response.content)
    return results

def check_detect(results):
    if results["image_id"] == "NA":
        return False
    else:
        return True
    
"""
if __name__ == "__main__":
    filename = capture_image()
    results = send_image_for_recognition(filename)
    print(check_detect(results))
"""