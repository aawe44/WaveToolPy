# -*- coding: utf-8 -*-
# 中文註解

#v2 add var_prm replace prm_value
#v3 use numpy.linspace replace range
#v4 增加中文註解，去除包含指定變數名稱的變數
#v5 增加Beep 去除不必要的註解
#v6 簡化程式，產生 _py.prm。用來改參數。



#===============================================
import os,subprocess,re
import winsound
import wave
import numpy as np
import matplotlib.pyplot as plt

#===============================================
def str_tuned(var_prm,prm_value):

    right_prm=var_prm[-5:]
    prm_tuned=var_prm.replace(right_prm,str(prm_value))
    #print(right_prm)
    #print(prm_tuned)
    return prm_tuned
#===============================================

def set_prm(prm_file_name,prm_var_name,prm_var_value):

    var_prm=prm_var_name
    i=prm_var_value

    f=open(prm_file_name,'r')
    lines=f.readlines()
    f.close()
    
    output_prm=prm_file_name.replace(".prm","_py.prm")

    output_file=open(output_prm,'w')

    i_hex=hex(int(i))
    i_hex=i_hex[2:].upper()
    
    for line in lines:
        # print(line)

        prm_tuned=line
        if var_prm in line:
            
            temp=line.split(".")
            temp=temp[1]
            temp=temp.split()
            temp=temp[0]

            if temp == var_prm:            
                print(line)
                prm_tuned=str_tuned(line,i_hex) +"\n"
                print(prm_tuned)
        
        output_file.write(prm_tuned)            

    output_file.close()

    return output_prm

#===============================================

def set_config(prm_file_name,prm_var_value):

    config_path=prm_file_name
    i=prm_var_value

    config_file=open(config_path,'r')
    config_lines=config_file.readlines()

    config_out_path=config_path.replace(".prm","_py.prm")
    config_out_file=open(config_out_path,'w')

    i_hex=hex(int(i))
    i_hex=i_hex[2:].upper()
    
    for config_line in config_lines:

        prm_tuned=config_line


        if "FVSAM_PARAM_NAME_TX_0" in config_line:
            prm_tuned= "FVSAM_PARAM_NAME_TX_0" + " " +output_prm +"\n"
            #print("FVSAM_PARAM_NAME_TX_0" + " " +output_prm)
            

        if "FVSAM_FNAME_LOUTWAV" in config_line:

            prm_tuned=config_line.replace(".wav","_v"+str(i_hex)+"_"+str(round(i/32767,5))+".wav")

        config_out_file.write(prm_tuned)

    config_out_file.close()

    return config_out_path


#===============================================
def my_wave_average(file,start_time, time_duration):

    #unit: ms                
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

    return np.average(abs(wave_data))



#===============================================
#隱藏CMD
if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
else:
    startupinfo = None

#===============================================
# Setting workspace
'''
current_path=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830"
os.chdir(current_path)  
'''

#input prm
prm_path=r"D:\JasonChen\Documents\v.4.0.7_release_20180830\input_prm_mm\d2t_handset_wb_micblock.prm"

config_path=r"D:\JasonChen\Documents\v.4.0.7_release_20180830\input_prm_mm\fvsam_wb_407_config.prm"

var_prm="MIC_VOL"

num_start=0
num_end=1
num_step=2

num_start=int(num_start*32767)
num_end=int(num_end*32767)

val=np.linspace(num_start,num_end,num_step)


#=========================================
for i  in val:
  
    output_prm =set_prm(prm_path,var_prm,i)
  
    config_out_path = set_config(config_path,i)
    
    
    sumulator_path= r"D:\JasonChen\Documents\v.4.0.7_release_20180830\fvsam_app_mi.exe "
    exe_cmd= sumulator_path + " "+ config_out_path
    #print(exe_cmd)

    subprocess.call(exe_cmd,startupinfo=startupinfo)


#========================================= end of val


wave_folder=r"D:\JasonChen\Documents\v.4.0.7_release_20180830\output_pcm\\"

files=os.listdir(wave_folder)

for file in files:

    if ".wav" in file:

        full_path=wave_folder + file

        wave_average=my_wave_average(full_path,1000,3000)

        wave_average=int(round(wave_average))

        print(file +" "+ str(wave_average))

#=========================================

winsound.Beep(600,100)
winsound.Beep(600,100)
winsound.Beep(600,100)
#其中600表示声音大小，1000表示发生时长，1000为1秒










