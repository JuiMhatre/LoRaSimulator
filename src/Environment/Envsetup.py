import Utils as utils
import EndDevices.device as device
import Environment.ChannelGroups as channel_groups
import NetworkServer.Scheduler as scheduler
import LoRaGateway.TransmissionGateway as gateway
from  Utils.TransmissionParameters import TransmissionParameter
import math
class Environment:
    def __init__(self):
        self.notcompleted=[]
        print("number of devices "+str(utils.nDevices))
        channelgroups = channel_groups.ChannelGroups()
        self.upstreamlist125 = channelgroups.getchannlesgroup("UP", 64, 200, 125, 902.3, 4, 0, 3)
        self.upstreamlist500 = channelgroups.getchannlesgroup("UP", 8, 1600, 500, 903.0, 4, 5, 6)
        self.downstreamlist500 = channelgroups.getchannlesgroup("DW", 8, 600, 500, 923.3, 4, 8, 13)
        self.total_energy=0
        self.total_delay=0
        self.pdr=0
        # self.setupChannelMap()
        # print("done creating channels")
        self.gateway = gateway.TransmissionGateway()
        self.setupEnv()
        self.setupChannelMap()
        
    def setupChannelMap(self):
        self.channelMap= {}
        for i in range(64):
            self.channelMap[self.upstreamlist125[i].startfreq] = self.upstreamlist125[i]
        for i in range(8):
            self.channelMap[self.upstreamlist500[i].startfreq]= self.upstreamlist500[i]


    def setupEnv(self):
        self.gateway.setup()
        for i in range(utils.nDevices):
            dev = device.Device(i)
            dev.setDistanceFromGateway(self.gateway.locX, self.gateway.locY)
            utils.READY_DEVICES.append(dev)


    def transmitToGateway(self, transparams, noOfRetry): 
        c_transparams = self.convertToLoRaTransParams(transparams)
        while(len(utils.READY_DEVICES)>0):            
            self.scheduleddevices_transparams = self.getSchedule(c_transparams)
            self.noOfRetry = noOfRetry
            for device in self.scheduleddevices_transparams.keys():
                if isinstance(self.scheduleddevices_transparams[device].CF, int):
                    self.scheduleddevices_transparams[device].CF= self.updateCFFromChannelNumber(self.scheduleddevices_transparams[device].CF)
                device.setTransmissionParams(self.scheduleddevices_transparams[device],self.noOfRetry)
                device.channel=self.channelMap[device.trans_params.CF]
                device.channel.devices_using_me.append(device)
                # print(str(device.deviceid)+"adding device to channel", device.channel.devices_using_me)
            self.selectDevicesToTransmitOnlySelectedByGW()
            self.startTransmission()
            
        self.getResults()
        reward =0
        if utils.OPTIMIZATION_TYPE == "ENERGY":
            reward = -1 * utils.total_energy
        if utils.OPTIMIZATION_TYPE == "LATENCY":
            reward = -1 * utils.total_delay
        if utils.OPTIMIZATION_TYPE == "PDR":
            reward = (utils.nDevices - len(self.notcompleted))/utils.nDevices
        return reward
    def convertToLoRaTransParams(self, trans_params):
        converted_transparams=[]
        for schedule  in trans_params:    
            schedulewise_deviceparams=[]        
            for device in schedule:
                tp = utils.TX_POW[int(device[0] * 14)]
                cf= int(device[1] * 71)
                cr = utils.CR[math.ceil(device[2] * 3)]
                sf = utils.SF[int(device[3] *5)]
                bw = utils.BANDWIDTH[math.ceil(device[4]) ] 
                newTransParm= TransmissionParameter(tp,cf, cr, sf, bw)
                schedulewise_deviceparams.append(newTransParm)
            converted_transparams.append(schedulewise_deviceparams)
        return converted_transparams
                
    def getSchedule(self,transparams):
        selected_Devices = self.gateway.invokeTransmissionByNS()
        actual_schedule={}
        
        for dev in selected_Devices:           
                
            if not( utils.DEV_SELECTED_SCHEDULE.get(dev.deviceid)is None):
                if utils.DEV_SELECTED_SCHEDULE[dev.deviceid]>= utils.MIN_SCHEDULES:
                    utils.READY_DEVICES.remove(dev)
                    self.notcompleted.append(dev)
                    continue
                actual_schedule[dev] = transparams[(utils.DEV_SELECTED_SCHEDULE[dev.deviceid])][dev.deviceid]
            else: 
                actual_schedule[dev] = transparams[0][dev.deviceid]
                utils.DEV_SELECTED_SCHEDULE[dev.deviceid]=0
            
            utils.DEV_SELECTED_SCHEDULE[dev.deviceid] =(utils.DEV_SELECTED_SCHEDULE[dev.deviceid]) + 1
        return actual_schedule
    
    def getResults(self):
        print("Average delay of each device is (secs) "+str(utils.total_delay/utils.nDevices))
        print("Average energy consumption  of each device is (J) "+str(utils.total_energy/utils.nDevices))
        print("Total energy (KJ)"+str(utils.total_energy/1e3))
        print("PDR "+str(100* (utils.nDevices - len(self.notcompleted))/utils.nDevices))
        
    def selectDevicesToTransmitOnlySelectedByGW(self):
        self.devicelist_ready = self.scheduleddevices_transparams.keys()
    
    def updateCFFromChannelNumber(self, channel_id):
        channel=None
        if  channel_id <64:
            channel= self.upstreamlist125[channel_id]
        else:
            channel= self.upstreamlist500[channel_id-64]
        return channel.startfreq
            
    def startTransmission(self):
        for dev in self.devicelist_ready:
            # print("Starting device "+str(dev.deviceid))
            if not dev.Transmission._started.is_set():
                dev.Transmission.start()
            else:
                dev.Transmission.startTransmission()
        for dev in self.devicelist_ready:
            dev.Transmission.join()
    
    
