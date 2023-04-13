import NetworkServer.Scheduler as scheduler
import Utils as utils
import NetworkServer.SchedulerInput as input
class TransmissionGateway:
    def setup(self):
        self.locX= utils.GATEWAY_LOCX
        self.locY = utils.GATEWAY_LOCY
        
        
    def invokeTransmissionByNS(self):
        noOfTasksReceived = len(utils.READY_DEVICES)
        return utils.READY_DEVICES[0:utils.GATEWAY_DEVICE_LIMIT]
        # if noOfTasksReceived > utils.GATEWAY_DEVICE_LIMIT:
        #     print("Gateway Overloaded!!  Dropping "+str(noOfTasksReceived - utils.GATEWAY_DEVICE_LIMIT)+" transmissions.")
        # input.SchedulerInput.getInput(input.SchedulerInput, devicelist[0:utils.GATEWAY_DEVICE_LIMIT],utils.ALGO_NAME)
        # # input.SchedulerInput.algorithm_name=utils.ALGO_NAME
        # # input.SchedulerInput.device_list = devicelist[0:utils.GATEWAY_DEVICE_LIMIT]
        # scheduler.Scheduler.inputToScheduler(scheduler.Scheduler,input)
        # return scheduler.Scheduler.sendtransmissionschedule(scheduler.Scheduler)