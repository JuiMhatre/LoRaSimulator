import threading
import time
import Utils as utils
exitFlag = 0

class Transmission (threading.Thread):
    def __init__(self, threadId,device):
      threading.Thread.__init__(self)
      self.threadID = threadId
      self.device = device
    def prepareTransmission(self):
       print("preparing transmission......")
       if self.device.data > 0:
           used_up_channel = self.device.used_channels.get(self.device.channel.startfreq, 0)
           if used_up_channel < utils.DWELL_TIME:
               remaining_dwell_time = utils.DWELL_TIME - used_up_channel
               if remaining_dwell_time > self.device.time_slot:
                   time_to_transmit = self.device.time_slot
               else:
                   time_to_transmit = remaining_dwell_time
               if self.CADOperation(): #channel sensing
                    data_sent = utils.BIT_RATE[self.device.trans_params.BW][self.device.trans_params.SF] * time_to_transmit
                    self.device.data = self.device.data - data_sent
                    time.sleep(time_to_transmit)
                    self.device.used_channels[self.device.channel.startfreq] = used_up_channel + time_to_transmit
                    self.resetCAD()
           else:
               ValueError("New Channel Required")
    def CADOperation(self): #https://lora-developers.semtech.com/documentation/tech-papers-and-guides/channel-activity-detection-ensuring-your-lora-packets-are-sent/how-to-ensure-your-lora-packets-are-sent-properly/
        inoperableTime = (32.0/self.device.trans_params.BW)/10**3; #milliseconds
        time.sleep(inoperableTime)
        cad_status_free = self.CADModeReady()
        self.CADProcess(cad_status_free)
        return cad_status_free


    def CADModeReady(self):
        valid_rssi_time = self.device.trans_params.getTsym()/10**3
        time.sleep(valid_rssi_time)
        if self.device.channel.taken:
            return False
    def CADProcess(self, cad_status_free):
        process_time = self.device.trans_params.getTsym()/(175 * 10**6)
        time.sleep(process_time)
        self.device.CadDone=True
        self.device.CadDetected=cad_status_free
        if cad_status_free:
            self.device.channel.taken = cad_status_free

    def resetCAD(self):
        self.device.channel.taken=False
        self.device.CadDone=False
        self.device.CadDetected=False

    def run(self):
      print ("Transmitting Device.... " + str(self.threadID))
      self.prepareTransmission()
      print ("Ending Transmission of device " + str(self.threadID))


