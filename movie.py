######################################
######################################
#Movie - Plots all of the channels contained within an image cube as a gif! 

#Functions: 

#movie          - Runs all Functions below. 
#readingrainbow - Reads data from the FITS file. Reads out RA, DEC.
#plotmovie      - Plots each frame of the image as a gif using ReadingRainbow


######################################
######################################


import os,sys
import matplotlib
import matplotlib.pyplot as plt
import pdb as pdb
from matplotlib import rcParams
import numpy as N
import matplotlib.gridspec as gridspec
from scipy import *
from matplotlib import rc
rc('text',usetex=False)
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#import pyfits
import astropy.io.fits as pyfits
from scipy import interpolate
from matplotlib.path import Path
from matplotlib.patches import FancyBboxPatch
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker

# import animation
import matplotlib.cm as cm
import matplotlib.animation as animation


#import scipy.io.array_import
from matplotlib.patches import Ellipse
from scipy.ndimage.interpolation import rotate

def movie(img, nchannels, svel, cmap, window, fitsdata = False):
       
    ############################################################


    ############################################################

    def readingrainbowCASA(img,ra_obj,de_obj,nchannels,sourcevel,flip=False,fitsdata=True):


        # ra_obj = right ascenscion in degrees. 11h 40m 30s = ((30/60+40)/60+11)*360/24 RA in hours -> degrees (float)
        # de_obj in degrees (float)
        # sourcevel in km/s = 2.88 km
        # img = is fits file name including directory

        csp = 2.99792e8 # c_speed of light in meters / s
        hdulist = pyfits.open(img)
        data = hdulist[0].data
        dims = data.shape

        ra0=hdulist[0].header['CRVAL1']
        dra=hdulist[0].header['CDELT1']
        de0=hdulist[0].header['CRVAL2']
        dde=hdulist[0].header['CDELT2']
        pra=hdulist[0].header['CRPIX1']
        pde=hdulist[0].header['CRPIX2']
        nu0=hdulist[0].header['RESTFRQ']
        nra = hdulist[0].header['NAXIS1']
        nde = hdulist[0].header['NAXIS2']
        nc = hdulist[0].header['NAXIS3']

        nu=hdulist[0].header['CRVAL3']
        dfr=hdulist[0].header['CDELT3']
        refnuind = hdulist[0].header['CRPIX3']


        if fitsdata == True:
            bmaj = hdulist[0].header['BMAJ']
            bmin = hdulist[0].header['BMIN']
            bpa = hdulist[0].header['BPA']
        else: 
            bmaj = 1.0
            bmin = 1.0
            bpa = 1.0


        hdulist.close()

        ravec = (N.arange(nra)+1-pra)*dra+ra0 # in degrees
        devec = (N.arange(nde)[::-1]+1-pde)*dde+de0 # in degrees

        # Convert to relative arcsec:
        ravec_rel = (ravec-ra_obj)*3600.0
        devec_rel = (de_obj-devec)*3600.0
        raarr_out,dearr_out = N.meshgrid(ravec_rel,devec_rel)

        frevec = ((N.arange(nc)+1)-refnuind)*dfr+nu
        velvec = (nu0-frevec)/nu0 * 2.99792e5 # km/s
        velvec = velvec[::-1]     

        centerchan = N.argmin(N.abs(velvec-sourcevel))
        # I think that this needs to be commented if you dropped stokes
        # if kept stokes, leave uncommented
        #data = data[0,:,:,:]  # Only one stokes parameter.
        if flip: data = data[::-1,:,:]

        data[N.isnan(data)] = 0.0 # set masked disk to zero (masked b/c has low sigma)
        cutch = N.round((nc - nchannels) / 2.0)
        datarr = data[int(centerchan-(nchannels-1)/2):int(centerchan-(nchannels-1)/2+nchannels)]
        velvec = velvec[int(centerchan-(nchannels-1)/2):int(centerchan-(nchannels-1)/2+nchannels)]
        velvec = velvec - sourcevel
        #datarr = data
        #velvec = data
        #pdb.set_trace()
        return datarr,nu0,raarr_out,dearr_out,dra,bmaj,bmin,bpa,velvec

    ############################################################

    ############################################################

    
    def RADEC(img):
        #Find RA and Dec for Disk based off Header file
        hdulist = pyfits.open(img)
        data = hdulist[0].data
        dims = data.shape
        ra0=hdulist[0].header['CRVAL1']
        de0=hdulist[0].header['CRVAL2']
        #print("RA and DEC")
        #print(ra0,de0)
        return ra0, de0

    

    ############################################################


    ############################################################
   
    ############################################################


   


    #########################################
    #########################################
    #########################################

    # How the font looks
    fts = 11
    rcParams['font.size'] = fts
    rcParams['font.family'] = 'serif'
    rcParams['font.weight'] = 'normal'

    # Plot colors
    # Feel free to change/play with! 
    # https://matplotlib.org/stable/users/explain/colors/colormaps.html
    colormap = plt.cm.get_cmap(cmap) #feel free to change the color!
    colorlab= 'k'
    coltick = 'k'

    # Sets position of the colorbar
    # I don't recommend changing this unless things start to look *weird*
    bw = 0.015
    pad = 0.013
    barsh = 1.0

    # I don't recommend setting this >100
    Nlevels = 75 # Number of colors to use in color map

    # if the code breaks with an error along the lines of "out of range" or something else that
    # doesn't make sense, decrease this number. 
    # I need to add a 'catch' for this in the code
    # number of channels to plot around center of line, +/- nchannels/2

    # increase or decrease to plot more/less of space
   


    #########################################
    #########################################
    #########################################
    img_name = img


    #########################################
    #########################################
    #########################################
    rapo, depo = RADEC(img)
    
    
    def plotmovie(nchannels,cmap,window,svel,rapo,depo,fitsdata):
        flip=False
        
        data_arr,linefreq,raarr,dearr,dra,bmaj,bmin,bpa,velvec \
            = readingrainbowCASA(img,rapo,depo,nchannels,svel, flip,fitsdata)
        fig, ax = plt.subplots()
        plt.axis('off')
        ims = []
        
        for i in range(nchannels):
            im = ax.imshow(data_arr[i,:,:], animated=True)
            ims.append([im])
            
    
        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=2500)
        ani.save('./userGifs/'+ img +'.gif')
        ani.save('movie.gif') #temp file


    rapo, depo = RADEC(img)
    
    colormap = plt.cm.get_cmap(cmap)
    plotmovie(nchannels, colormap, window,svel,rapo,depo,fitsdata) 
    return 
    



