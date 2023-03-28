from  Utils.TransmissionParameters import TransmissionParameter as trans_params
import Utils as utils
class Scheduler:
    def __init__(self):
        pass
    def inputToScheduler(self,devlist_ready_to_transmit):
        self.devlist=devlist_ready_to_transmit
        pass
    def sendtransmissionschedule(self):
        self.dev_wise_params={}
        for dev in self.devlist:
            self.dev_wise_params[dev]= trans_params(utils.TX_POW[14],902.3,4,7,125) #get from algorithm
        return self.dev_wise_params