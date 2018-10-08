# -*- coding: utf-8 -*-
# 中文註解

#v2 add var_prm replace prm_value
#v3 use numpy.linspace replace range
#v4 增加中文註解，去除包含指定變數名稱的變數



#===============================================
import os,subprocess,re
import numpy as np

def str_tuned(var_prm,prm_value):

    right_prm=var_prm[-5:]
    prm_tuned=var_prm.replace(right_prm,str(prm_value))
    #print(right_prm)
    #print(prm_tuned)
    return prm_tuned
#===============================================

if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
else:
    startupinfo = None

#===============================================

current_path=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830"
os.chdir(current_path)  

prm_path=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830\input_prm_mm\E5-SKYPE-Handfree-wb-dt-ISSUE_20180927_tuned.prm"
#print(prm_path)
f=open(prm_path,'r')
lines=f.readlines()
f.close()

config_path=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830\input_prm_mm\fvsam_wb_407_config.prm"
config_file=open(config_path,'r')

var_prm="MIN_EQ_RE_EST_1"

num_start=0
num_end=1
num_step=4

#num_step=int((num_end-num_start)/num_step+1)

num_start=int(num_start*32767)
num_end=int(num_end*32767)

val=np.linspace(num_start,num_end,num_step)


#=========================================
for i  in val:

    output_prm=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830\input_prm_mm\E5-SKYPE-Handfree-wb-dt-ISSUE_20180927_tuned_v2.prm"
    #print(output_prm)
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
        '''            
        if "EAD_THR_FC" in line:
            #print(line)
            prm_tuned=str_tuned(line,6666) +"\n"
            #print(prm_tuned)
        '''
        
        output_file.write(prm_tuned)            

    output_file.close()

    #======================================================

    config_path=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830\input_prm_mm\fvsam_wb_407_config.prm"
    config_file=open(config_path,'r')
    config_lines=config_file.readlines()

    config_out_path=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830\input_prm_mm\fvsam_wb_407_config_out.prm"
    config_out_file=open(config_out_path,'w')

    for config_line in config_lines:

        prm_tuned=config_line
        
        if "FVSAM_FNAME_LOUTWAV" in config_line:

            prm_tuned=config_line.replace("v0","v"+str(i_hex)+"_"+str(round(i/32767,2)))

        config_out_file.write(prm_tuned)

    config_out_file.close()

    exe_cmd=r"D:\Work\20180919_XM_issue\v.4.0.7_release_20180830\fvsam_app_mi.exe "+ config_out_path
    #print(exe_cmd)

    subprocess.call(exe_cmd,startupinfo=startupinfo)


#========================================= end of val



