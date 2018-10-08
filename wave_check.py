import wave
import matplotlib.pyplot as plt
import numpy as np

def my_wave_average(file,start_time, time_duration):
        
    f = wave.open(file, "rb")

    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
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

    wave_data = np.frombuffer(str_data, dtype=np.short)
    wave_data.shape = -1, nchannels
    wave_data = wave_data.T

    frame_start=int(start_time*framerate/1000)
    frame_duration=int(time_duration*framerate/1000)
    
    wave_data=wave_data[0,frame_start:(frame_start+frame_duration)]

    '''
    plt.figure()
    plt.plot(abs(wave_data))
    plt.show()
    plt.close()
    '''
    
    return np.average(abs(wave_data))
    
#==============================
    
file = r"vptx_out.is880.B3.04.wav"

test_time=np.linspace(0,10000,11)

for i in test_time:

    print(i)

    wave_average=my_wave_average(file,i,1000)       #unit: ms

    print(wave_average)












