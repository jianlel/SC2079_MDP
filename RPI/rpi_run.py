from queue import Queue
from android_link import *
from stmv3 import *
import serial
import time

filename = "/home/pi/Desktop/test.jpg"
server_url = "http://192.168.15.18:5000/"
commands = None

def connect():
    serial_link = serial.Serial(
        "/dev/ttyUSB0",
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2,
    )
    print("Connected to STM32")

def send(message: str):
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
    print(list(cmd_q.queue))

    while(True):
        command = q.get()
        if command == "FIN":
            print("End of command queue")
            break
        elif command == "DET":
            print("Sending for detection")
            time.sleep(1)
            capture_image()
            results = send_image_for_recognitition(filename)
            if check_detect(results) == True:
                print(results)
            else:
                print("image rec failed")
        else:
            send(command)
            while not ack_check():
                time.sleep(0.0001)

    print("Run finished")

if __name__ == "__main__":
    commands = ["WX100", "FIN"]

    for task in commands:
        for movement in task:
            cmd_q.put(movement)

    serial_link = serial.Serial(
        "/dev/ttyUSB0",
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2,
    )
    print("Connected to STM32")

    run_path(cmd_q)     