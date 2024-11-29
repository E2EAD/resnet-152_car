"""
manager.py
Main script for the application. This is the core script including the main loop.
"""
import cv2
import time
import os
import numpy as np
import threading

from input_manager import InputManager
from inference import Inference
from variables import Command, CurrentState, Mode
from gui import Gui
from data_manager import DataManager
from network import Network

class Manager():
    def __init__(self,mode: Mode, connection: Network, application_state: CurrentState, data_manager: DataManager):
        """Inits the manager

        Args:
            mode (Mode): Mode in which the application is running
            connection (Network): Network connection
            application_state (CurrentState): Current application state
            data_manager (DataManager): Data management object
        """    
        self.mode = mode
        self.connection = connection
        self.application_state = application_state
        self.data_manager = data_manager

        self.key = InputManager(data_manager, mode)
        self.gui = Gui()

    def main_loop(self):
        """Main loop for the application. All other functionality is called from this loop.
            In each iteration the current user inputs are checked and the current video stream
            is received. Also the new commands are sent back to the car.
        """        
        condition = Command.forward 
        prediction = Command.no_command

        # loop_cnt = 0
        # print('here is manager, start main loop.')


        while True:
            # compute main loop freq
            # if loop_cnt == 0:
            #     time_start = time.time()
            #     loop_cnt += 1
            # elif loop_cnt == 100:
            #     time_finish = time.time()
            #     loop_cnt = 0
            #     period = time_finish - time_start
            #     freq = 100 / period
            #     print(f'100 loops spend {period}s, loop freq is {freq}Hz.')
            # else:
            #     loop_cnt += 1
            #     print(f'loop_cnt is {loop_cnt}')

            # print(f'loop_cnt is {loop_cnt}')

            data = self.connection.receive_image()

            if self.key.quit:
                print("Break")
                break

            if self.mode == Mode.inference:
                prediction = self.application_state.get_last_predicted()["action"]

            action = self.key.get_action()

            condition = self.key.get_condition(condition)

            image = self.gui.transform_image(data)

            self.application_state.set_current(image, condition)
            
            if action != Command.no_command:
                self.connection.send_command(action)

                if self.key.recording:
                    self.data_manager.append_data(image, action.value, condition.value)

            elif self.key.self_driving and prediction != Command.no_command:
                self.connection.send_command(prediction)

            # print(f'here is manager main loop, action={action},key.self_driving={self.key.self_driving},prediction={prediction}')
            # print(f'if send self driving command:{self.key.self_driving and prediction != Command.no_command}')
            self.gui.show_state(np.copy(image), condition, prediction, self.key.recording, self.key.self_driving)

