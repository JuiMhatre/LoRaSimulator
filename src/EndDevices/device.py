import random
import Utils as utils
import time
from Utils.TransmissionParameters import TransmissionParameter as transparams
import EndDevices.Transmission as Transmission
import random
from scipy.stats import norm
import math
import numpy as np

class Device:
    def __init__(self, deviceid=None):
        # print("setting up device")
        self.data=utils.DEVICE_DATA
        self.used_channels= {}
        self.deviceid=deviceid
        self.Transmission = Transmission.Transmission(deviceid,self)
        self.trans_params = transparams(TP=0,CF=0,CR=4,SF=7,BW=125)
        self.time_slot=utils.TIME_SLOT
        self.CadDone=False
        self.CadDetected =False;
        self.CadRetry=3
        self.locX = random.randint(utils.NETWORK_AREA_MIN_X, utils.NETWORK_AREA_MAX_X)
        self.locY = random.randint(utils.NETWORK_AREA_MIN_Y, utils.NETWORK_AREA_MAX_Y)
        self.time_taken=0
        self.energy=0
        
        
    def setTransmissionParams(self, transparam, noOfRetry):
        self.trans_params = transparam
        self.CadRetry = noOfRetry        
        self.rssi = self.getRSSI()
        

    def setChannel_Time(self,channel_Freq,time_slot):
        self.channel = channel_Freq
        self.time_slot = time_slot
        
    def getPathLoss(self):
        return utils.LPLD0 - 10 * utils.GAMMA * math.log10(self.distance / utils.D0) - np.random.normal(-utils.VARIANCE, utils.VARIANCE)
    
    def setDistanceFromGateway(self, gateway_x, gateway_y):
        self.distance = np.sqrt((self.locX - gateway_x) * (self.locX - gateway_x) + (self.locY - gateway_y) * (self.locY - gateway_y))
        self.pathLoss = self.getPathLoss()

    def getRSSI(self):
        return self.trans_params.TP - self.pathLoss
