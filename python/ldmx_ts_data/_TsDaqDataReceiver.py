"""
Title: DataReceiver.py

Author: Kieran Wall (University of Virginia) -> wer2ct@virginia.edu

Created: 7/15/2024

Last Modified: 8/2/2024

Description: Shell/outline of data receiver for LDMX Trigger Scintillator live visualization. Takes ADC/TDC data-frame (to be constructed) from FPGA and constructs pydm variables for use in GUI.

How to run me: From the top level directory of TDAQ_VIS, run "python3 scripts/TsTop.py". You will then need to turn on the frame generator from the GUI that pops up. The "Process" function will then run for every frame that is received at a rate set inside of the GUI. 
"""

#Imports
import linecache
import random
import pyrogue as pr
import numpy as np
import sys
import collections as cols
import time
import BitVector as bv



#Data Receiver Class Initialization
class TsDaqDataReceiver(pr.DataReceiver):
    
    #Initialization, define variables including pyrogue locals
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #some dummy variables just to have something here...
        self.frame_start = time.time()
        self.nframes = 0

        #linearization encoding
        self.nbins=[0,16, 36, 57, 64]
        self.edges=[0,34,158,419,517,915,1910,3990,4780,7960,15900,32600,38900, 64300, 128000, 261000, 350000]
        self.sense=[3,6,12,25, 25, 50, 99, 198,198, 397, 794, 1587, 1587, 3174, 6349, 12700]
        
        self.add(pr.LocalVariable(
            name = "Receiving",
            value = 0,
            description = "DataReciever Running?"
        ))
        self.add(pr.LocalVariable(
            name = "ChnlData",
            value = np.zeros([12]),
            description = "PE data for histogram"
        ))
        self.add(pr.LocalVariable(
            name = "EvtCount",
            value = 0,
            description = "Counts the event. Current stand in for broken timing"
        ))
        self.add(pr.LocalVariable(
            name = "ChannelBins",
            value = np.arange(0,12),
            description = "Channel Bins"
        ))
        self.add(pr.LocalVariable(
            name = "AvgPE",
            value = 0.,
            description = "PE averaged over activate channels"
        ))
        self.add(pr.LocalVariable(
            name = "ChannelActive",
            value = 0,
        ))
        #Active Channel Variables -> Default Zero
        for i in range(12):
            self.add(pr.LocalVariable(
                name = f'Chnl[{i}]',
                value = 0))
            self.add(pr.LocalVariable(
                name = f'ChnlVal[{i}]',
                value = 0.))

    #Utility Functions#
    def rand_line(self): #input TestVec file, output random line from TestVec as np array, channel is first entry
        data_entry = np.empty([13])
        random_line = linecache.getline('python/ldmx_ts_data/TestVecBetter.txt', random.randint(1,3000))
        x = random_line.split(",")
        x.pop()
        for i in range(13):
            data_entry[i] = int(x[i])
        linecache.clearcache()
        return(data_entry)
    
    def ADC_plus_TDC(self, ADC, TDC): #input ADC and TDC and return combined word
        ADC_b = bv.BitVector(intVal=ADC, size = 8)
        TDC_b = bv.BitVector(intVal=TDC, size = 6)
        return(ADC_b + TDC_b)
              
    def linearization(self,w): #input word, output PE
        
        #Linearization script is Rory's, I am still not 100% confident it is functioning properly, but better than nothing for now 
        adc_b = w.shift_right(6)
        adc = int(adc_b)
        rr=adc//64
        v1=adc%64
        ss=(v1>self.nbins[1])+(v1>self.nbins[2])+(v1>self.nbins[3])
        charge=self.edges[4*rr+ss]+(v1-self.nbins[ss])*self.sense[4*rr+ss]+self.sense[4*rr+ss]/2-1
        return ((charge-36)*.00625*1.1556136857680435)
            
    #Process, define function to be run everytime a new frame is received#
    def process(self,frame):
        self.EvtCount += 1
        self.Receiving.set(1)
    
        #Pulling random data from TestVec
        n_channels_active = random.randint(1,5)
        event_total = 0.0
        channel_array = np.zeros([12])
        for i in range(n_channels_active):
            data_entry = self.rand_line()
            chnl_num = int(data_entry[0])
            chnl_total = 0.0
            for i in range(1,5):
                conc = self.ADC_plus_TDC(int(data_entry[i]),int(data_entry[i+6]))
                chrg = self.linearization(conc)
                chnl_total += round(chrg,4)
            #print(f'{self.Channel.get()} -> {chnl_total}')
            channel_array[chnl_num] = chnl_total
        
        #Setting Rogue Variables
        print(channel_array)
        event_total = np.sum(channel_array)
        avgPE = round(np.average(channel_array),4)
        self.ChnlData.set(channel_array)
        self.AvgPE.set(avgPE)
        #print(self.AvgPE.get())
        #print(self.ChnlData.get())

        #Setting Channel Rogue Variables
        actives = np.nonzero(channel_array)
        self.ChannelActive.set(np.count_nonzero(channel_array))
        #print(actives)


        for i in range(12):
            self.ChnlVal[i].set(np.round(channel_array[i],4))
            if np.isin(i,actives):
                self.Chnl[i].set(1)
            else:
                self.Chnl[i].set(0)
        """
        Sample ADC and TDC with expected

        adcs=[95,148,145,128,109,64] #191.037 (broken)
        tdcs=[8,62,62,62,62,62]
        adcs2=[150,145,128,109,95,81] #192.714
        tdcs2=[62,62,62,62,62,62]
        adcs3=[144,136,119,103,87,73] #148.053
        tdcs3=[62,62,62,62,62,62]
        adcs4=[151,145,129,110,96,81] #197.693
        tdcs4=[62,62,62,62,62,62]
        adcs5=[154,148,132,113,100,84] #221.214
        tdcs5=[62,62,62,62,62,62]
        adcs6=[73,159,154,139,121,104] #273.48
        tdcs6=[8,62,62,62,62,62]
        adcs7=[159,152,137,119,103,88] #258.495
        tdcs7=[62,62,62,62,62,62]
        """
