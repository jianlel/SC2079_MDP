import bluetooth
import requests
import ast
import os
import json
import serial
from multiprocessing import Process, Manager
from queue import Queue
import time
from stmv3 import *
from rpi_run import *
server_url = 'http://192.168.15.18:5000/path'  # URL of your Flask server
stitch_url = 'http://192.168.15.13:5000/stitch'
client_socket=None
server_socket=None
obs_ids = [-1,-1,-1,-1,-1,-1,-1,-1]
cmd_q = Queue()
img_q = Queue()
coord_q = Queue()
id_q = Queue()

def android_connect():
    global client_socket
    global server_socket
    try:
        os.system("sudo hciconfig hci0 piscan")
        
        #init server socket
        server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_socket.bind(("", bluetooth.PORT_ANY))
        server_socket.listen(1)

        #params
        port = server_socket.getsockname()[1]
        #port = 1
        print(server_socket.getsockname())
        uuid = '94f39d29-7d6d-437d-973b-fba39e49d4ee' # UUID for Serial Port Profile (SPP)

        bluetooth.advertise_service(server_socket, "BluetoothServer", service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        print(f"Waiting for connection on RFCOMM channel {port}")

        client_socket, client_info = server_socket.accept()
        print(f"Accepted connection from {client_info}")
        
    except Exception as e:
        print(e)
        server_socket.close()
        client_socket.close()
        
def android_disconnect():
    try:
        server_socket.shutdown(socket.SHUT_RDWR)
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        server_socket.close()
        client_socket=None
        server_socket=None
    except Exception as e:
        print(e)

def android_receive():
    try:
        tmp = client_socket.recv(1024)
        msg = tmp.strip().decode("utf-8")
        print(msg)
        return msg
    except OSError as e:
        print(e)
        raise e
                             
def forward_data_to_algo_server(json_data):
    actual_json_data = json.loads(json_data)
    obs_list = actual_json_data["value"]["obstacles"]
    print(obs_list)
    body = {"obstacles": obs_list, "big_turn": 0, "robot_x": 1, "robot_y": 1, "robot_dir": 0, "retrying": False}
    try:
        #json_data = data.decode('utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_url, json=body,
                                 #headers=headers
                                 )
        if response.status_code == 200:
            print("Data sent to server successfully")
            return response.content
        else:
            print(f"Failed to send data to server. Response code: {response.status_code}")
            return response
    except Exception as e:
        print(f"Error sending data to server: {e}")

def convert_to_list(s):
    ls = ast.literal_eval(s)
    return ls

def update_x_y_direction(command, x_coord, y_coord, direction):
    if command[:2] == "FR":
        # Facing North
        if direction == 0:
            x_coord = x_coord + 3
            y_coord = y_coord + 1
        # Facing East
        elif direction == 2:
            x_coord = x_coord + 3
            y_coord = y_coord - 1
        # Facing South
        elif direction == 4:
            x_coord = x_coord - 3
            y_coord = y_coord - 1
        # Facing West
        else:
            x_coord = x_coord - 3
            y_coord = y_coord + 1
        direction = (direction + 2) % 8
    
    elif command[:2] == "FL":
        # Facing North
        if direction == 0:
            x_coord = x_coord - 1
            y_coord = y_coord + 3
        # Facing East
        elif direction == 2:
            x_coord = x_coord + 3
            y_coord = y_coord + 1
        # Facing South
        elif direction == 4:
            x_coord = x_coord + 1
            y_coord = y_coord - 3
        # Facing West
        else:
            x_coord = x_coord - 3
            y_coord = y_coord - 1
        direction = (direction - 2) % 8
        if direction == -2:
            direction = 6
            
    elif command[:2] == "BR":
        # Facing North
        if direction == 0:
            x_coord = x_coord + 3
            y_coord = y_coord - 1
        # Facing East
        elif direction == 2:
            x_coord = x_coord - 1
            y_coord = y_coord - 3
        # Facing South
        elif direction == 4:
            x_coord = x_coord - 1
            y_coord = y_coord + 3
        # Facing West
        else:
            x_coord = x_coord + 3
            y_coord = y_coord + 1
        direction = (direction - 2) % 8
        if direction == -2:
            direction = 6
    
    elif command[:2] == "BL":
        # Facing North
        if direction == 0:
            x_coord = x_coord - 3
            y_coord = y_coord - 1
        # Facing East
        elif direction == 2:
            x_coord = x_coord - 1
            y_coord = y_coord + 3
        # Facing South
        elif direction == 4:
            x_coord = x_coord + 3
            y_coord = y_coord + 1
        # Facing West
        else:
            x_coord = x_coord + 1
            y_coord = y_coord - 3
        
        direction = (direction + 2) % 8
    
    elif command[:2] == "FW":
        distance = int(command[2])
        # Facing North
        if direction == 0:
            y_coord = y_coord + distance
        # Facing East
        elif direction == 2:
            x_coord = x_coord + distance
        # Facing south
        elif direction == 4:
            y_coord = y_coord - distance
        # Facing West
        else:
            x_coord = x_coord - distance
        
    elif command[:2] == "BW":
        distance = int(command[2])
        # Facing North
        if direction == 0:
            y_coord = y_coord - distance
        # Facing East
        elif direction == 2:
            x_coord = x_coord - distance
        # Facing south
        elif direction == 4:
            y_coord = y_coord + distance
        # Facing West
        else:
            x_coord = x_coord + distance
            
    return x_coord, y_coord, direction

def recv_wait():
    global obs_counts
    global commands
    global cmd_q
    global obs_ids
    while True:
        msg_str = ""
        try:
            msg_str = android_receive()
        except OSError:
            print(e)
                
        if msg_str is None:
            continue

        print("test")
        msg_tmp= json.loads(msg_str)


        ## Command: Set obstacles ##
        if msg_tmp['cat'] == "obstacles":
            data = forward_data_to_algo_server(msg_str)
            
            proper_data = json.loads(data)["data"]
            commands = proper_data["commands"]
            print(commands)
            
            for i in range(len(commands)):
                if commands[i].startswith("SNAP"):
                    obs_ids[obs_counts]= commands[i][4]
                    detection = commands[i][6]
                    with open('/home/pi/Desktop/detection.txt', 'a') as f:
                        f.write(str(detection) + "\n")
                    obs_counts += 1
                    commands[i] = "DET"
            with open('/home/pi/Desktop/obs_ids.txt', 'w') as f:
                for item in obs_ids:
                    f.write(str(item)+'\n')
        
            
            for i in range(len(commands)):
                if commands[i] == "DET" or commands[i] == "FIN":
                    pass
                else:
                    commands[i] += "0"
                    
            # If inside lab, BL, BR, FL, FR should be 000
            # If outside lab, BL, BR, FL, FR should be 200
            # So if inside lab, comment this whole part out
            
            for i in range(len(commands)):
                if commands[i].startswith("BL"):
                    commands[i] = "BL200"
                
                elif commands[i].startswith("BR"):
                    commands[i] = "BR200"
                    
                elif commands[i].startswith("FL"):
                    commands[i] = "FL200"
                    
                elif commands[i].startswith("FR"):
                    commands[i] = "FR200"
            
            
            print(commands)
            for command in commands:
                cmd_q.put(command)
            
        ## Command: Start Moving ##
        elif msg_tmp['cat'] == "control":
            if msg_tmp['value'] == "start1":
                # Start task 1
                run_path(cmd_q)
            elif msg_tmp['value'] == "start2":
                # Start task 2
                run_path(cmd_q)
                
            """
            elif msg_temp['value] == "start2":
                # Start task 2
                print("starting")
            """
                
def android_send(message):
        try:
            msg = json.dumps(message)
            msg += "\n"
            msg = msg.encode("utf-8")
            client_socket.send(msg)
            print(f"Sent to Android: {msg}")
        except OSError as e:
            print(e)

def android_image_sender():
        while True:
            # Retrieve from queue
            try:
                #msg comes from image server
                msg = img_q.get(timeout=0.5)
                print(msg)
            except Exception as e:
                print(e)
                break

            try:
                android_send(msg)
            except OSError:
                print(" img process error")
                break
            
def android_coordinate_sender():
    while True:
        # Retrieve from queue
        try:
            #msg comes from rpi coord queue
            msg = coord_q.get(timeout=0.5)
            print(msg)
        except Exception as e:
            print(e)
            break

        try:
            android_send(msg)
        except OSError:
            print("Coord send error")
            break
            
def stm_send(message: str):
    serial_link.write(message.encode("utf-8"))
    print("Sent to STM32: " + message)

def ack_check():
    message = serial_link.readline().strip().decode("utf-8")
    print("Received from STM32: " + message)
    if message.startswith("ACK"):
        return True
    else:
        return False
    
def run_path(q):
    global img_q
    global coord_q
    x_coord = 0
    y_coord = 0
    direction = 0
    count=0
    while(True):
        command = q.get()
        if command=="FIN":
            requests.post("http://192.168.15.13/task2")
            print("End of command queue")
            break
        elif command=="DET":
            
            print("sending for detection")
            #time.sleep(1)
            filename = capture_image()
            #filename = f"/home/pi/Desktop/test_{count}.jpg" 
            send_image_for_recognition(filename)
            
            #img_id = results["image_id"]
            #obs_jpg = results["obstacle_id"]
            #obs_id = obs_jpg[0]
            #msg = {"cat" : "image-rec" , "value": {"image_id": img_id , "obstacle_id": obs_id}}
            #count += 1
            #print(msg)
            #if check_detect(results)==True:
            #    img_q.put(msg)
            #    time.sleep(1)
            #    android_image_sender()
            #else:
            #    print("img rec error")
            #    continue
        else:
            stm_send(command)
            while not ack_check(): time.sleep(0.01)
            if(command=="DT100"):
                requests.post("http://192.168.15.13/task2")
                
                
            #x_coord, y_coord, direction = update_x_y_direction(command, x_coord, y_coord, direction)
            # Create the json format here using x, y, direction
            #print(x_coord)
            #print(y_coord)
            #print(direction)
            #location_data = {
            #    "cat": "location",
            #    "value" : {
            #        "x": x_coord,
            #        "y": y_coord,
            #        "d": direction
            #    }
            #}
            
            # Push the json into the queue
            #coord_q.put(location_data)
            # Call the process to send the coords
            #android_coordinate_sender()
              
            
    print("Run finished")
    

if name == "main":
    obs_counts=0
    try:        
        android_connect()
        serial_link = serial.Serial("/dev/ttyUSB0",baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=2,)
        proc_recv_android = Process(target = recv_wait())
        #proc_send_android_image = Process(target = android_image_sender())
        #proc_send_android_coords = Process(target = android_coordinate_sender())
        
        proc_connect_android.start()
        #proc_send_android_image.start()
        #proc_send_android_coords.start()
        
    except Exception as e:
        print(e)
        android_disconnect()