import Environment.Channel as channel

class ChannelGroups():
    def creategroup(self, type, nChannels, freq_diff, BW, startfreq,CR, minDR,maxDR):
        channels_list=[]
        for ch in range(nChannels):
            channels_list.append(channel.Channel(type, BW, startfreq, CR, minDR, maxDR))
            startfreq=startfreq+(freq_diff/100)

        return channels_list
    def getchannlesgroup(self,type, nChannels, freq_diff, BW, startfreq,CR, minDR,maxDR):
        return self.creategroup(type, nChannels, freq_diff, BW, startfreq,CR, minDR,maxDR)

