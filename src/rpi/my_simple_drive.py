"""
my_simple_drive.py
Contains all the necessary functions to control the motors for driving

SYB:需要重写小车运动部分代码，运动逻辑是某种运动指令对应固定的四轮电机输入（可由实验确定L，R的值），持续某个时间。
"""
from variables import CurrentState, Directions
# from distance import Distance  # 未用到超声波测距模块
import json
import requests
import serial


class SimpleDrive(object):

    def __init__(self, currentState: CurrentState, car_port='/dev/ttyAMA0'):
        """Init

        Args:
            currentState (CurrentState): Current State
        """

        self.L = 0
        self.R = 0
        # self.car_ip = car_ip
        self.current_command = {'T': 1, 'L': 0, 'R': 0}  # JSON command

        self.currentState = currentState
        self.ser = serial.Serial(car_port, baudrate=115200, dsrdtr=None)
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        # self.distance = Distance(self.currentState)

    def stop(self):
        """
        Stop driving.
        """
        self.L = 0
        self.R = 0
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)

        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')

    def forward(self):
        """
        Driving forward.
        """
        self.L = 0.3
        self.R = 0.39
        # speed = self.currentState.get_speed() 保留此语句，未来可能需要通过其他条件改变速度
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)
        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')


    def reverse(self):
        """
        Driving backward with normal speed.
        """
        self.L = -0.3
        self.R = -0.39
        # speed = self.currentState.get_speed() 保留此语句，未来可能需要通过其他条件改变速度
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)
        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')

    def left(self):
        """
        Driving to the left.
        """
        self.L = 0
        self.R = 0.39
        # speed = self.currentState.get_speed() 保留此语句，未来可能需要通过其他条件改变速度
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)
        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')

    def right(self):
        """
        Driving to the right.
        """
        self.L = 0.3
        self.R = 0
        # speed = self.currentState.get_speed() 保留此语句，未来可能需要通过其他条件改变速度
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)
        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')

    def turn_left(self):
        """
        Turning left.
        """
        self.L = -0.3
        self.R = 0.39
        # speed = self.currentState.get_speed() 保留此语句，未来可能需要通过其他条件改变速度
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)
        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')

    def turn_right(self):
        """
        Turning right.
        """
        self.L = 0.3
        self.R = -0.39
        # speed = self.currentState.get_speed() 保留此语句，未来可能需要通过其他条件改变速度
        # load motor pwm
        self.current_command['T'] = 1
        self.current_command['L'] = self.L
        self.current_command['R'] = self.R
        # send JSON command
        # url = "http://" + self.car_ip + "/js?json=" + json.dumps(self.current_command)
        # response = requests.get(url)
        self.ser.write(json.dumps(self.current_command).encode() + b'\n')
        #print('json command has been sent by pi.')

    def move(self):
        """
        Main driving loop
        """
        while True:
            # self.distance.measure_distance()

            direction = self.currentState.get_direction()

            if (direction == Directions.stop):
                self.stop()
            elif direction == Directions.reverse:
                self.reverse()
            elif direction == Directions.forward:
                self.forward()
            elif direction == Directions.left:
                self.left()
            elif direction == Directions.right:
                self.right()
            elif direction == Directions.turn_left:
                self.turn_left()
            elif direction == Directions.turn_right:
                self.turn_right()

    def read_serial(self):
        '''
        might needed while logging imu data
        '''
        while True:
            data = self.ser.readline().decode('utf-8')
            if data:
                print(f"Received: {data}", end='')
