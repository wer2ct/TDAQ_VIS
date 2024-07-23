"""
Title: DataReceiver.py

Author: Kieran Wall (University of Virginia) -> wer2ct@virginia.edu

Created: 7/15/2024

Last Modified: 7/16/2024

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
        self.nbins_ = [0,16,36,57,64]
        self.edges_ = [0,34,158,419,517,915,1910,3990,4780,7960,15900,32600,38900,64300,128000,261000,350000]
        self.sense_ = [3,6,12,25,25,50,99,198,198,397,794,1587,1578,3174,6349,12700]
        
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
            name = "ChannelBins",
            value = np.arange(0,12),
            description = "Channel Bins"
        ))
        self.add(pr.LocalVariable(
            name = "Channel",
            value = 0,
            description = "Which channel is reading out data in this frame"
        ))
        self.add(pr.LocalVariable(
            name = "chargePE",
            value = 0.0,
            description = "What is the PE of the channel being read (over 6 clock cycles)",
        ))
            


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
        #print(w)
        ADC = w.shift_right(6)
        #print(ADC)
        rr = int(ADC) // 64 
        v1 = int(ADC) % 64 
        ss = 1*(v1>self.nbins_[1]) + 1*(v1>self.nbins_[2]) + 1*(v1>self.nbins_[3])
        charge = (self.edges_[4*rr+ss]) + ((v1-self.nbins_[ss])*self.sense_[4*rr+ss]) + (self.sense_[4*rr+ss]/2) - 1
        return((charge)*0.00625)
    
    #Process, define function to be run everytime a new frame is received#
    def process(self,frame):
        self.Receiving.set(1)
        n_channels_active = random.randint(1,5)
        event_total = 0.0
        channel_array = np.zeros([12])
        for i in range(n_channels_active):
            data_entry = self.rand_line()
            chnl_num = int(data_entry[0])
            chnl_total = 0.0
            for i in range(1,6):
                conc = self.ADC_plus_TDC(int(data_entry[i]),int(data_entry[i+6]))
                chrg = self.linearization(conc)
                chnl_total += round(chrg,4)
            #print(f'{self.Channel.get()} -> {chnl_total}')
            channel_array[chnl_num] = chnl_total

        event_total = np.sum(channel_array)
        self.ChnlData.set(channel_array)
        print(self.ChnlData.get())
        
        
            
        


            
        """    
        charge = self.linearization(self.ADC_plus_TDC(150,62))
        print(charge)
        testADC = ([64,148,145,128,109,95])
        testTDC = ([8,62,62,62,62,62])
        for i in range(6):
            conc = self.ADC_plus_TDC(testADC[i],testTDC[i])
            chrg = self.linearization(conc)
            print(chrg)
            total += chrg
        print(f'total->{total}')
        #print(f'diff->{expected-total}\n')
        """
        
        
        
        
        
        
            
            
        
       
            
            
            
        
        
        
        
        
        
