"""
inference_model.py
Extends the network model with a forward function to infere single images
"""
import torch
import sys
sys.path.append(r'E:\TJRAIL\car\resnet-152_car\src')
from computer.network.model import Net
from variables import Command

# 改变当前工作目录
# import os
# os.chdir('E:\\TJRAIL\\car\\SelfDrivingElegooCar-master\\src\\computer\\network')
# from model import Net

class InferenceNet(Net):

    def forward(self, observation: torch.Tensor, condition: int) -> torch.Tensor:
        """Forward pass for inference

        Args:
            observation (torch.Tensor): Image of size 224x224x3
            condition (int): Condition

        Returns:
            torch.Tensor: Prediction
        """        

        x = self.resnet_model(observation)

        if condition == Command.left:
            x = self.fc[1](x)
        elif condition == Command.right:
            x = self.fc[2](x)
        else:
            x = self.fc[0](x)

        return x
