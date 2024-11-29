'''
my_imu_log.py
'''
import json
import requests
import time
import datetime

class ImuLog(object):

    def __init__(self, log_file,car_ip='192.168.43.164',log_freq=30):
        """Init
        """
        self.log_file = log_file
        self.car_ip = car_ip
        self.log_freq = log_freq
        self.pitch = 0
        self.roll = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0
        self.mx = 0
        self.my = 0
        self.mz = 0
        self.temp = 0

    def parse_data(self,data):
        # data format is {"T": value, "r": value, "p": value,
        # "ax": value, "ay": value, "az": value,
        # "gx": value, "gy": value, "gz": value,
        # "mx": value, "my": value, "mz": value, "temp": value}
        imu_data = json.loads(data)
        self.pitch = imu_data.get("p", 0)
        self.roll = imu_data.get("r", 0)
        self.ax = imu_data.get("ax", 0)
        self.ay = imu_data.get("ay", 0)
        self.az = imu_data.get("az", 0)
        self.gx = imu_data.get("gx", 0)
        self.gy = imu_data.get("gy", 0)
        self.gz = imu_data.get("gz", 0)
        self.mx = imu_data.get("mx", 0)
        self.my = imu_data.get("my", 0)
        self.mz = imu_data.get("mz", 0)
        self.temp = imu_data.get("temp", 0)

        # Log data to file
        timestamp = str(time.time())
        with open(self.log_file, "a") as f:
            f.write(
                f"{timestamp},{self.pitch},{self.roll},{self.ax},{self.ay},{self.az},\
                {self.gx},{self.gy},{self.gz},{self.mx},{self.my},{self.mz},{self.temp}\n")

    def log_data(self):
        """
        Main logging loop
        """
        period = 1.0 / self.log_freq
        while True:
            try:
                url = "http://" + self.car_ip + "/js?json=" + '{"T":126}'
                response = requests.get(url)
                data = response.text
                print(f"Received: {data}")
                self.parse_data(data)
            except Exception as e:
                print(f"Error processing http data: {e}")
            time.sleep(period)


