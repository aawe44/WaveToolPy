import wave,os



Path = os.getcwd()

FileName = "vptx_out.is880.20181011.00.ch1.wav"

outFilePrefix = FileName.split(".wav")[0]
inFile = Path +"\\"+ FileName
outFile = Path + "\\output_pcmcut\\" + outFilePrefix


timeTbl = [7733,42137] #in ms WB
NoiseTbl = ["mensa", "mensa_proc", "hoth", "hoth_proc"] #in ms
waveLen = 30000 #in ms
count = 0

origAudio = wave.open(inFile,'r')
frameRate = origAudio.getframerate()
nChannels = origAudio.getnchannels()
sampWidth = origAudio.getsampwidth()
frames = origAudio.getnframes()

print ("Frame Rate: " +  str(frameRate))
print ("Channel Number: " +  str(nChannels))
print ("Sample Width: " +  str(sampWidth))
print ("Sample frames: " +  str(frames))


for start in timeTbl:
 
    startFr = start*frameRate/1000
    origAudio.setpos(int(start*frameRate/1000))

    chunkData = origAudio.readframes(int(waveLen*frameRate/1000))
    chunkAudio = wave.open(outFile +"_"+NoiseTbl[count]+'.wav','w')
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)
    chunkAudio.writeframes(chunkData)
    chunkAudio.close()
    count=count+1
	
origAudio.close()




