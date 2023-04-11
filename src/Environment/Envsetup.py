import Utils as utils
import EndDevices.device as device
import Environment.ChannelGroups as channel_groups
import NetworkServer.Scheduler as scheduler
import LoRaGateway.TransmissionGateway as gateway
class Environment:
    def __init__(self):
        print("creating channels")
        channelgroups = channel_groups.ChannelGroups()
        self.upstreamlist125 = channelgroups.getchannlesgroup("UP", 64, 200, 125, 902.3, 4, 0, 3)
        self.upstreamlist500 = channelgroups.getchannlesgroup("UP", 8, 1600, 500, 903.0, 4, 5, 6)
        self.downstreamlist500 = channelgroups.getchannlesgroup("DW", 8, 600, 500, 923.3, 4, 8, 13)
        self.total_energy=0
        self.total_delay=0
        self.pdr=0
        # self.setupChannelMap()
        print("done creating channels")
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


    def transmitToGateway(self): 
        while(len(utils.READY_DEVICES)>0):
            self.schedule, self.noOfRetry = self.gateway.invokeTransmissionByNS(utils.READY_DEVICES)
            for device in self.schedule.keys():
                self.schedule[device].CF= self.updateCFFromChannelNumber(self.schedule[device].CF)
                device.setTransmissionParams(self.schedule[device],self.noOfRetry)
                device.channel=self.channelMap[device.trans_params.CF]
                device.channel.devices_using_me.append(device)
            self.selectDevicesToTransmitOnlySelectedByGW()
            self.startTransmission()
        self.getResults()
        
    def getResults(self):
        print("Average delay of each device is (s) "+str(utils.total_delay/utils.nDevices))
        print("Average energy consumption  of each device is (A) "+str(utils.total_energy/utils.nDevices))
        print("PDR "+str(100* (utils.nDevices - len(utils.READY_DEVICES))/utils.nDevices))
    def selectDevicesToTransmitOnlySelectedByGW(self):
        self.devicelist_ready = self.schedule.keys()
    
    def updateCFFromChannelNumber(self, channel_id):
        channel=None
        if  channel_id <64:
            channel= self.upstreamlist125[channel_id]
        else:
            channel= self.upstreamlist500[channel_id-64]
        return channel.startfreq
            
    def startTransmission(self):
        for dev in self.devicelist_ready:
            print("Starting device "+str(dev.deviceid))
            if not dev.Transmission._started.is_set():
                dev.Transmission.start()
            else:
                dev.Transmission.startTransmission()
        for dev in self.devicelist_ready:
            dev.Transmission.join()
    
    
