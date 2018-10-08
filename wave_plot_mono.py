import wave
import matplotlib.pyplot as plt
import numpy as np

def my_plot(file,start_time, time_duration):
        
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

    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, nchannels
    wave_data = wave_data.T

    frame_start=int(start_time*framerate)
    frame_duration=int(time_duration*framerate)
    
    wave_data=wave_data[0,frame_start:(frame_start+frame_duration)]

    plt.figure()
    plt.plot(wave_data)
    plt.show()
    
    

#==============================
    
file = r"vptx_out.is880.B3.04.wav"
#file = r"D:\Work\20180718_Recording_Crash_QA\ReleaseTest\check_no_sound\vptx_out.is880.B3.04.wav"


my_plot(file,5,1)       #unit: sec


