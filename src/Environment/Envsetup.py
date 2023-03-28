import Utils as utils
import EndDevices.device as device
import Environment.ChannelGroups as channel_groups
# from src.NetworkServer.Scheduler import Scheduler as scheduler
import NetworkServer.Scheduler as scheduler

class Environment:
    def __init__(self):
        print("creating channels")
        channelgroups = channel_groups.ChannelGroups()
        self.upstreamlist125 = channelgroups.getchannlesgroup("UP", 64, 200, 125, 902.3, 4, 0, 3)
        self.upstreamlist500 = channelgroups.getchannlesgroup("UP", 8, 1600, 500, 903.0, 4, 5, 6)
        self.downstreamlist500 = channelgroups.getchannlesgroup("DW", 8, 600, 500, 923.3, 4, 8, 13)
        # self.setupChannelMap()
        print("done creating channels")
        self.setupEnv()
        self.setupChannelMap()

    def setupChannelMap(self):
        self.channelMap= {}
        for i in range(64):
            self.channelMap[self.upstreamlist125[i].startfreq] = self.upstreamlist125[i]


    def setupEnv(self):
        self.devicelist = []
        for i in range(utils.nDevices):
            dev = device.Device(i)
            self.devicelist.append(dev)


    def invokeTransmissionByNS(self):
        scheduler.Scheduler.inputToScheduler(scheduler.Scheduler, self.devicelist)
        self.schedule = scheduler.Scheduler.sendtransmissionschedule(scheduler.Scheduler)
        for device in self.schedule.keys():
            device.setTransmissionParams(self.schedule[device])
            device.channel=self.channelMap[device.trans_params.CF]
        self.startTransmission()

    def startTransmission(self):
        for dev in self.devicelist:
            dev.Transmission.start()
