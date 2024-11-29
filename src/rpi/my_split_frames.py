'''
my_split_frames.py
'''
# 导入必要的模块
import socket
import struct
import select
import cv2

# 假设 CurrentState 类是从其他模块导入的
from variables import CurrentState

class SplitFrames(object):
    def __init__(self, socket: socket.socket, connection: socket.socket, current_state: CurrentState):
        self.socket = socket
        self.connection = connection
        self.current_state = current_state
        self.count = 0
        self.end_stream = False

    def send_frame(self, frame):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, encoded_image = cv2.imencode('.jpg', frame, encode_param)

        if not result:
            print("Failed to encode image")
            return
        
        data = encoded_image.tobytes()

        try:
            # Send the length of the JPEG stream first
            self.connection.sendall(struct.pack('<L', len(data)))
            # Send the image data
            self.connection.sendall(data)
        except BrokenPipeError:
            print("Connection closed by client.")
            self.end_stream = True
            return
        
        self.count += 1

        # Receive command
        readable, _, _ = select.select([self.socket], [], [], 0)
        if readable:
            message_length = struct.calcsize('<L')
            message = self.connection.recv(message_length)
            if message:
                message = struct.unpack('<L', message)[0]

                if message == 8:
                    self.end_stream = True
                    self.current_state.reset_stop_timer()
                else:
                    self.current_state.set_direction(message)
                    self.current_state.set_direction(message)
