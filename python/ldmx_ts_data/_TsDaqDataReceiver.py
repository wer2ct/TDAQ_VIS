"""
Title: DataReceiver.py

Author: Kieran Wall (University of Virginia) -> wer2ct@virginia.edu

Created: 7/15/2024

Last Modified: 7/16/2024

Description: Shell/outline of data receiver for LDMX Trigger Scintillator live visualization. Takes ADC/TDC data-frame (to be constructed) from FPGA and constructs pydm variables for use in GUI.

How to run me: TBD 
"""

#Imports
import pyrogue as pr
import numpy as np
import sys
import collections as cols
import time

#Data Receiver Class Initialization
class TsDaqDataReceiver(pr.DataReceiver):
    
    #Initialization, define variables including pyrogue locals
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #some dummy variables just to have something here...
        
        self.frame_start = time.time()
        self.nframes = 0
        self.add(pr.LocalVariable(
            name = "GrabFrame",
            value = "False",
            description = "Should we grab frame or not?"
        ))
        self.add(pr.LocalVariable(
            name = "Receiving",
            value = 0,
            description = "DataReciever Running?"
        ))
        self.add(pr.LocalVariable(
            name = "HitCount",
            value = 0,
            description = "Hits Recorded in Frame"
        ))

        
    #Process, define function to be run everytime a new frame is received
    def process(self,frame):
        self.HitCount += 1
        print("Frame received\n")
        self.Receiving.set(1)
        
        
            
            
        
       
            
            
            
        
        
        
        
        
        
