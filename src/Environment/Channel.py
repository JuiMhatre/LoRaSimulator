
class Channel():
    def __init__(
            self,
            type,#upstream/downstream
            BW,
            startfeq,
            CR,
            minDR,
            maxDR):
        self.type=type
        self.BW=BW
        self.startfreq=startfeq
        self.CR = CR
        self.minDR = minDR
        self.maxDR = maxDR
        self.taken=False
        self.devices_using_me=[]