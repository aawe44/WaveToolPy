import wave
import matplotlib.pyplot as plt
import numpy as np

file = r"D:\Work\20180718_Recording_Crash_QA\ReleaseTest\check_no_sound\01_vptx_out.HSWB.TS.tuned.wav"
#file = r"D:\Work\20180718_Recording_Crash_QA\ReleaseTest\check_no_sound\vptx_out.is880.B3.04.wav"


f = wave.open(file, "rb")

# (nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

print ("Frame Rate: " +  str(framerate))
print ("Channel Number: " +  str(nchannels))
print ("Sample Width: " +  str(sampwidth))
print ("Sample frames: " +  str(nframes))


str_data = f.readframes(nframes)
f.close()

wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, nchannels
wave_data = wave_data.T
time = np.arange(0, nframes) * (1.0 / framerate)

figure = plt.gcf() # get current figure
#figure.set_size_inches(8*20, 6)

duration = nframes/float(framerate)
xticks = np.arange(0, duration, 60)
plt.subplot(211).set_xticks(xticks)
plt.plot(time, wave_data[0])

plt.subplot(212).set_xticks(xticks)
plt.plot(time, wave_data[3], c="g")
plt.xlabel("time (seconds)")

plt.show()
plt.close(figure)









