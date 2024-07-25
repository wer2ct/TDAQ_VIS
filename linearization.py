import numpy as np

def linearization(adc_array):
    nbins=[0,16, 36, 57, 64]
    edges=[0,34,158,419,517,915,1910,3990,4780,7960,15900,32600,38900, 64300, 128000, 261000, 350000]
    sense=[3,6,12,25, 25, 50, 99, 198,198, 397, 794, 1587, 1587, 3174, 6349, 12700]

    SUMMER=0.0
    
    for adc in adc_array[:4]:
        rr=adc//64
        v1=adc%64
        ss=(v1>nbins[1])+(v1>nbins[2])+(v1>nbins[3])
        charge=edges[4*rr+ss]+(v1-nbins[ss])*sense[4*rr+ss]+sense[4*rr+ss]/2-1
        SUMMER+=(charge-36)*.00625*1.1556136857680435

    return(SUMMER)

def main():
    adcs1=[64,148,145,128,109,95]
    expected_1 = 191.037
    print(f'\n1. Linearized: {linearization(adcs1)} Expected: {expected_1}\n')
    
    adcs2=[150,145,128,109,95,81]
    expected_2 = 192.714
    print(f'2. Linearized: {linearization(adcs2)} Expected: {expected_2}\n')
    
    adcs3=[144,136,119,103,87,73]
    expected_3 = 148.053
    print(f'3. Linearized: {linearization(adcs3)} Expected: {expected_3}\n')
    
    adcs4=[151,145,129,110,96,81]
    expected_4 = 197.693
    print(f'4. Linearized: {linearization(adcs4)} Expected: {expected_4}\n')
    
    adcs5=[154,148,132,113,100,84]
    expected_5 = 221.214
    print(f'5. Linearized: {linearization(adcs5)} Expected: {expected_5}\n')

    adcs6=[73,159,154,139,121,104]
    expected_6 = 273.48
    print(f'6. Linearized: {linearization(adcs6)} Expected: {expected_6}\n')
    
    adcs7=[65,149,146,129,111,97]
    expected_7 = 199.988
    print(f'7. Linearized: {linearization(adcs7)} Expected: {expected_7}\n')

    adcs8=[159,152,137,119,103,88]
    expected_8 = 258.495
    print(f'8. Linearized: {linearization(adcs8)} Expected: {expected_8}\n')

main()
    
