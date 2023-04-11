import NetworkServer.Scheduler as scheduler
import Utils as utils
class TransmissionGateway:
    def setup(self):
        self.locX= utils.GATEWAY_LOCX
        self.locY = utils.GATEWAY_LOCY
        
    def invokeTransmissionByNS(self, devicelist):
        noOfTasksReceived = len(devicelist)
        # if noOfTasksReceived > utils.GATEWAY_DEVICE_LIMIT:
        #     print("Gateway Overloaded!!  Dropping "+str(noOfTasksReceived - utils.GATEWAY_DEVICE_LIMIT)+" transmissions.")
        scheduler.Scheduler.inputToScheduler(scheduler.Scheduler, devicelist[0:utils.GATEWAY_DEVICE_LIMIT])
        return scheduler.Scheduler.sendtransmissionschedule(scheduler.Scheduler)