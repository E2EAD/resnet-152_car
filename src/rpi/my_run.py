"""
my_run.py
Main script to run the car.
"""
import socket
import struct
import time
from datetime import datetime
import os
import yaml
import threading
import cv2

from my_simple_drive import SimpleDrive
from my_split_frames import SplitFrames
from variables import CurrentState
from my_imu_log import ImuLog


def main():
    """Main driving function
    """
    with open("config.yml") as cf:
        config = yaml.safe_load(cf.read())

    # setup connection
    client_socket = socket.socket()
    client_socket.connect((config["ip"], 8000))

    # setup the current state
    current_state = CurrentState()

    # setup driving thread
    simple_drive = SimpleDrive(current_state, config["car_port"])
    simple_drive_thread = threading.Thread(target=simple_drive.move)
    simple_drive_thread.setDaemon(True)
    simple_drive_thread.start()

    # Setup camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, config["fps"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["resolutionX"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["resolutionY"])

    try:
        splitter = SplitFrames(client_socket, client_socket, current_state)  # 使用同一个 socket 对象
        while True:
            start = time.time()  # log start time
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            splitter.send_frame(frame)

            finish = time.time()  # log finish time

            if splitter.end_stream:
                break

    finally:
        cap.release()
        simple_drive.ser.close()
        try:
            client_socket.close()
        except:
            pass

        finish = time.time()
        # print('Sent %d images in %d seconds at %.2ffps' % (
        #     splitter.count, finish-start, splitter.count / (finish-start)))


if __name__ == '__main__':
    main()
