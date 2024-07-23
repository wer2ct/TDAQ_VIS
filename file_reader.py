"""A quick test of Rogue functionality will be drawing lines from the TestVec.dat and processing them. This script creates an output text file with only channel ADC and TDC information (TestVectBetter.txt). This file will be inputted to Rogue to select the lines"""

import numpy as np

def file_reader():
    f = open("TestVec.txt", "r")
    o = open("python/ldmx_ts_data/TestVecBetter.txt", "w")
    for l in f:
        """
        if(l == 'b\n'):
            print("found b\n")
            o.write("\n")
        """
        if(len(l) > 15):
            o.write(l)  
    f.close()
    o.close()
                       
def main():
    file_reader()

main()
    
