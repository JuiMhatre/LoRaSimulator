
class TransmissionParameter:
    def __init__(self, TP, CF, CR, SF, BW):
        self.TP= TP
        self.CF= CF
        self.CR = CR
        self.SF= SF
        self.BW = BW

    def getTsym(self):
        return 2 ** self.SF / self.BW; #duration that is the airtime of a single LoRa chirp