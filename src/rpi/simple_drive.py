"""
simple_drive.py
Contains all the necessary functions to control the motors for driving

SYB:需要重写小车运动部分代码，运动逻辑是某种运动指令对应固定的四轮电机输入（可由实验确定L，R的值），持续某个时间。
"""
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice

from variables import CurrentState, Directions
from distance import Distance


class SimpleDrive(object):

    def __init__(self, currentState: CurrentState):
        """Init

        Args:
            currentState (CurrentState): Current State
        """        
        ENA = 12
        ENB = 13
        IN1 = 16
        IN2 = 20
        IN3 = 26
        IN4 = 19

        self.driveRight = PWMOutputDevice(ENA, True, 0, 1000)  # 转速
        self.driveLeft = PWMOutputDevice(ENB, True, 0, 1000)
        self.forwardLeft = PWMOutputDevice(IN1)  # 方向
        self.reverseLeft = PWMOutputDevice(IN2)
        self.reverseRight = PWMOutputDevice(IN3)
        self.forwardRight = PWMOutputDevice(IN4)
        
        self.currentState = currentState

        self.distance = Distance(self.currentState)

    def stop(self):
        """
        Stop driving.
        """
        self.forwardLeft.value = False
        self.reverseLeft.value = False
        self.forwardRight.value = False
        self.reverseRight.value = False
        self.driveLeft.value = 0
        self.driveRight.value = 0

    def forward(self):
        """
        Driving forward.
        """
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = True
        self.reverseRight.value = False
        speed = self.currentState.get_speed()
        self.driveLeft.value = 1.0 * speed
        self.driveRight.value = 1.0 * speed

    def reverse(self):
        """
        Driving backward with normal speed.
        """
        self.forwardLeft.value = False
        self.reverseLeft.value = True
        self.forwardRight.value = False
        self.reverseRight.value = True
        speed = self.currentState.speed
        self.driveLeft.value = speed
        self.driveRight.value = speed

    def left(self):
        """
        Driving to the left.
        """
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = True
        self.reverseRight.value = False
        speed = self.currentState.get_speed()
        self.driveLeft.value = 0.2 * speed
        self.driveRight.value = 1.0 * speed

    def right(self):
        """
        Driving to the right.
        """
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = True
        self.reverseRight.value = False
        speed = self.currentState.get_speed()
        self.driveLeft.value = 1.0 * speed
        self.driveRight.value = 0.2 * speed

    def turn_left(self):
        """
        Turning left.
        """
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = False
        self.reverseRight.value = True
        speed = self.currentState.get_speed()
        self.driveLeft.value = 1.0 * speed
        self.driveRight.value = 1.0 * speed

    def turn_right(self):
        """
        Turning right.
        """
        self.forwardLeft.value = False
        self.reverseLeft.value = True
        self.forwardRight.value = True
        self.reverseRight.value = False
        speed = self.currentState.get_speed()
        self.driveLeft.value = 1.0 * speed
        self.driveRight.value = 1.0 * speed

    def move(self):
        """
        Main driving loop
        """        
        while True:
            self.distance.measure_distance()

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
