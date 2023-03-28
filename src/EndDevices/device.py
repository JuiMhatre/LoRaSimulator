import random

import Utils as utils
import time
from Utils.TransmissionParameters import TransmissionParameter as transparams
import EndDevices.Transmission as Transmission
class Device:
    def __init__(self, deviceid=None):
        print("setting up device")
        self.data=10*1000000*8 #10MB in bits
        self.used_channels= {}
        self.deviceid=deviceid
        self.Transmission = Transmission.Transmission(deviceid,self)
        self.trans_params = transparams(TP=0,CF=0,CR=4,SF=7,BW=125)
        self.time_slot=0
        self.CadDone=False
        self.CadDetected =False;


    def setTransmissionParams(self, transparam):
        self.trans_params = transparam

    def setChannel_Time(self,channel_Freq,time_slot):
        self.channel = channel_Freq
        self.time_slot = time_slot

