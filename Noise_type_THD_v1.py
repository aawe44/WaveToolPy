#2018/10/16 add select channel and num_of_noise
#2018/10/17 add stable time; add my_array_check to delete small duration
#2018/10/18 add xlsx output


import wave
import numpy as np
from openpyxl import Workbook

#==================================================
def my_array_check(endpt,minTestTime):
    if np.size(endpt, 0) != 2:
        print("error ndim")
        return 0

    n = np.size(endpt, 1)
    temp = []
    temp_start=temp_end=[]
    for i in range(0, n):
        if abs(endpt[0, i] - endpt[1, i]) > minTestTime:
            temp_start=np.append(temp_start,endpt[0,i])
            temp_end = np.append(temp_end, endpt[1, i])

    temp=np.vstack((temp_start,temp_end))
    return temp

#==================================================
def endpoint_dect(wave_data):

    # split the duration of noise
    diff=[]
    flag=0

    for i in range(0,nframes):
        if abs(wave_data[i])>0:
            flag=1
        else:
            flag=0
        diff.append(flag)

    x=np.array(diff)

    # check startpoint/ endpoit
    startpoint=[]
    endpoint=[]

    x=np.diff(x)

    for i in range(x.size):
        if x[i]>0:
            startpoint=np.append(startpoint,i)
        if x[i]<0:
            endpoint=np.append(endpoint,i)
    '''
    print(startpoint,endpoint)
    print(len(startpoint),len(endpoint))
    print(type(wave_data))
    print(len(wave_data))
    '''
    if len(startpoint) ==(len(endpoint)+1):
        endpoint = np.append(endpoint, len(wave_data))

    output=np.vstack((startpoint,endpoint))
    output=my_array_check(output,30000)

    return output
# end of  endpoint_dect
#==================================================

file = "debugInfo_QDSP_iS880_V4_7_8_Google_DebugInfo_04_B4_HAWB_NEW_Jason_v2_prm.wav"
num_of_noise=8
stable_time=20000  #unit: ms
f = wave.open(file, "rb")
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

print ("Frame Rate: " +  str(framerate))
print ("Channel Number: " +  str(nchannels))
print ("Sample Width: " +  str(sampwidth))
print ("Sample frames: " +  str(nframes))

str_data = f.readframes(nframes)
f.close()

str_data = np.frombuffer(str_data, dtype=np.short)
str_data.shape = -1, nchannels
str_data = str_data.T

time = np.arange(0, nframes) * (1.0 / framerate)

all_channel_val=[]
wave_data=[]

#define select channels: [HighCar, High, LowHigh, High2, High3]
select_channels=range(2,7)

for i in select_channels:
    print("Running channel: ",i+1)
    wave_data=str_data[i]
#    print(endpoint_dect(wave_data)/framerate)

    endpoint=endpoint_dect(wave_data)
    endpoint=np.array(endpoint,dtype=np.int)

    channel_val=[]
    temp=[]

    #print(endpoint.shape)
    for val in endpoint.T:
        wav_duration=wave_data[val[0]+stable_time:val[1]]
        wav_duration = wav_duration.compress((wav_duration!=0).flat)

        wav_max=max(wav_duration)
        wav_min=min(wav_duration)
        #print(wav_max, wav_min)
        temp=np.vstack((wav_max,wav_min))
        channel_val=np.append(channel_val,temp)
    all_channel_val=np.append(all_channel_val,channel_val)
all_channel_val=all_channel_val.reshape(5,num_of_noise*2)

#print(all_channel_val)
print('Done !!!')

#==================================================
file=file.replace(".wav","")
outputfile="Noise_type_THD_"+file+".txt"
np.savetxt(outputfile,all_channel_val,fmt='%d',delimiter=' ')

#==================================================
output_xlsx="Noise_type_THD_"+file+".xlsx"

wb=Workbook()
ws=wb.active

m=np.size(all_channel_val, 0)
n=np.size(all_channel_val, 1)

for i in range(0,m):
    for j in range(0,n):
        ws.cell(row=i+1,column=j+1,value=all_channel_val[i,j])

wb.save(output_xlsx)

#==================================================

