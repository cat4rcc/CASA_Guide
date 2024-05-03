# Beam Size Calculator 
# imports 

#Used in make your own Image Section Not yet created
import numpy as np 
import pdb as pdb
import os 


def beamsize (imgname): 
    def find_noise_beam(imgname,type='line'):
        # get the beam from the dirty image to figure out
        # how the uvtaper should be applied accoring to Loomis' function
        bmax_obs = imhead(imagename=imgname+'.image',mode="get",hdkey="bmaj")['value']
        bmin_obs = imhead(imagename=imgname+'.image',mode="get",hdkey="bmin")['value']
        bpa_obs = imhead(imagename=imgname+'.image',mode="get",hdkey="bpa")['value']#*180/np.pi #radian to deg
        if abs(bpa_obs) < 5.0:
            bpa_obs = bpa_obs*180.0/np.pi
        else:
            bpa_obs = bpa_obs
        return bmax_obs,bmin_obs,bpa_obs,noise

    bmax_obs, bmin_obs, bpa_obs, noise = find_noise_beam(imagename+'.dirty',type='line')
    print(bmax_obs,bmin_obs,bpa_obs,noise)
    return(bmax_obs,bmin_obs,bpa_obs)