import wave
import matplotlib.pyplot as plt
import numpy as np

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
          
    output=np.vstack((startpoint,endpoint))
    return output
# end of  endpoint_dect
#==================================================

file = r"D:\Work\20180718_Recording_Crash_QA\ReleaseTest\check_no_sound\01_vptx_out.HSWB.TS.tuned.wav"
#file = r"D:\Work\20180718_Recording_Crash_QA\ReleaseTest\check_no_sound\vptx_out.is880.B3.04.wav"

f = wave.open(file, "rb")

params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

'''
print ("Frame Rate: " +  str(framerate))
print ("Channel Number: " +  str(nchannels))
print ("Sample Width: " +  str(sampwidth))
print ("Sample frames: " +  str(nframes))
'''

str_data = f.readframes(nframes)
f.close()

str_data = np.fromstring(str_data, dtype=np.short)
str_data.shape = -1, nchannels
str_data = str_data.T

time = np.arange(0, nframes) * (1.0 / framerate)

all_channel_val=[]
wave_data=[]

for i in range(3,7):
    
    wave_data=str_data[i]
    #print(endpoint_dect(wave_data)/framerate)
    
    endpoint=endpoint_dect(wave_data)
    endpoint=np.array(endpoint,dtype=np.int)

    channel_val=[]
    temp=[]

    for val in endpoint.T:

        wav_duration=wave_data[val[0]:val[1]]
        wav_duration = wav_duration.compress((wav_duration!=0).flat)

        wav_max=max(wav_duration)
        wav_min=min(wav_duration)
        
        temp=np.vstack((wav_max,wav_min))
        channel_val=np.append(channel_val,temp)

    all_channel_val=np.append(all_channel_val,channel_val)

print(all_channel_val.reshape(4,8))
print('Done !!!')

np.savetxt('Noise_type_THD.txt',all_channel_val.reshape(4,8),fmt='%d',delimiter=' ')





