"""
mom0.py

This script is meant to 
 1. Read in line data from a fits file
 2. Calculate the moment zero map by integrating over velocity space
 3. plot the moment zero map 
The moment zero image does not use masked data

Overview of functions and their purpose:
 RADEC Finds the RA and DEC from the Fits File.
 minmax 

"""
import os,sys
import matplotlib
import matplotlib.pyplot as plt
import pdb as pdb
from matplotlib import rcParams
import numpy as np
from numpy import ma
import matplotlib.gridspec as gridspec
from scipy import *
from matplotlib import rc
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.colors import LogNorm
import astropy.io.fits as pyfits
from scipy import interpolate
from matplotlib.path import Path
from matplotlib.patches import FancyBboxPatch
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker
from matplotlib.patches import Ellipse
from scipy.ndimage.interpolation import rotate
from numpy.linalg import inv


############################################################
def readingrainbow(img,ra_obj,de_obj,nchannels,sourcevel,flip=False,mask=False):

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


    if mask == False:
        bmaj = hdulist[0].header['BMAJ']
        bmin = hdulist[0].header['BMIN']
        bpa = hdulist[0].header['BPA']
    else: 
        bmaj = 1.0
        bmin = 1.0
        bpa = 1.0

    hdulist.close()

    ravec =(np.arange(nra)+1-pra)*dra+ra0
    devec = (np.arange(nde)[::-1]+1-pde)*dde+de0 # in degrees

    # Convert to relative arcsec:
    ravec_rel = (ravec-ra_obj)*3600.0
    devec_rel = (de_obj-devec)*3600.0
    raarr_out,dearr_out = np.meshgrid(ravec_rel,devec_rel)

    frevec = ((np.arange(nc)+1)-refnuind)*dfr+nu
    velvec = (nu0-frevec)/nu0 * 2.99792e5 # km/s

    # if kept stokes, leave uncommented
    #data = data[0,:,:,:]  # Only one stokes parameter.
    if flip: data = data[::-1,:,:]

    data[np.isnan(data)] = 0.0 # set masked disk to zero (masked b/c has low sigma)
    #cutch = np.round((nc - nchannels) / 2.0)

    return data,nu0,raarr_out,dearr_out,dra,bmaj,bmin,bpa,velvec

def RADEC(img):
    #Find RA and Dec for Disk based off Header file
    hdulist = pyfits.open(img)
    data = hdulist[0].data
    dims = data.shape
    ra0=hdulist[0].header['CRVAL1']
    de0=hdulist[0].header['CRVAL2']
    print("RA and DEC")
    print(ra0,de0)
    return ra0, de0
    
def minmax(img,rapo,depo):
    #Find the Minimum and Maximum contour values for Disk. 
    data_arr,linefreq,raarr,dearr,dra,bmaj,bmin,bpa,velvec \
            = readingrainbow(img,rapo,depo,'nchannels',svel,flip=False,mask=False)
        
    data_arr = data_arr * 1e3 # convert from Jy -> mJy
    contmin = data_arr.min()
    contmax = data_arr.max()
    return contmin, contmax
    

def calcmom0(img,rapo,depo,svel):

    data_arr,linefreq,raarr,dearr,dra,bmaj,bmin,bpa,velvec \
            = readingrainbow(img,rapo,depo,'nchannels',svel,flip=False,mask=False)

    data_arr = data_arr * 1e3 # convert from Jy -> mJy


    # you can also multiply data_arr by mask_arr if you want to apply the mask
    mzero = np.trapz((data_arr),x=velvec,axis=0)#(data_arr[:,,],x=velvec)   

    # flip the mom0 map if necessary (will depend on direction of velocity vector)
    if abs(mzero.min()) > abs(mzero.max()): mzero = mzero*-1.0
    
    return mzero,raarr,dearr,velvec,bmaj,bmin,bpa





def plotmom0(fig,ax0,img,\
             rapo,depo,svel,\
             fts,colormap,colorlab,coltick,\
             bw,pad,barsh,\
             Nlevels,ellicol,\
             window,contvals,contlab,add_colorbar):
   
    mzero,raarr,dearr,velvec,bmaj,bmin,bpa = calcmom0(img,rapo,depo,svel) 
    # ONLY plot the data in the window you are plotting. 
    # if you plot all of the data, the pdf size is very large
    drv = np.where(np.abs(raarr[0,:]) <= window*1.1)[0]

    ddv = np.where(np.abs(dearr[:,0]) <= window*1.1)[0]

    CS2 = ax0.contourf(raarr[drv[0]:drv[-1],ddv[0]:ddv[-1]],\
                       dearr[drv[0]:drv[-1],ddv[0]:ddv[-1]],\
                       mzero[drv[0]:drv[-1],ddv[0]:ddv[-1]],\
                       contvals, cmap=colormap, extend='both')


    ellpo = window-1.0 # ellipse position -- center of where the beam will go
    ells = Ellipse(xy=[ellpo,-ellpo], width=bmin*3600.0, height=bmaj*3600.0, angle=bpa*-1,zorder=300)
    ells.set_facecolor(ellicol)
    ells.set_edgecolor(ellicol)
    ax0.add_artist(ells)


    ax0.set_xlim(window,-1*window)
    ax0.set_ylim(-1*window,window)

    # plot a small star where the star is
    ax0.scatter(0,0,marker='*',c='white',edgecolor='dimgrey')

    ax0.set_ylabel(r"$\Delta\theta_{\rm Dec}''$",fontsize=fts+1,labelpad=3.0,)
    ax0.set_xlabel(r"$\Delta\theta_{\rm Ra}''$",fontsize=fts+1,labelpad=3.0,)
    if add_colorbar == True:
        pt = ax0.get_position().bounds
        cax = fig.add_axes([pt[0]+pt[2]+pad-bw/2, pt[1]+pt[3]*(1.0-barsh)/2.0, bw, pt[3]*barsh])
        cbar = plt.colorbar(CS2,ax=cax,ticks=contlab,orientation='vertical')
        #cbar.ax.set_xticklabels(FormatStrFormatter('%.0f').format_ticks(contlab))
        cbar.ax.set_ylabel(r'mJy beam$^{-1}$',fontsize=fts,color='k',labelpad=15.0,rotation=270)
        cax.axis('off')



    return 


    #####################################
    #####################################
    ####################################

def mom0(imnames, svel, color_map, ellicol, labcol, window):

    fts = 11
    rcParams['font.size'] = fts
    rcParams['font.family'] = 'serif'
    rcParams['font.weight'] = 'normal'

    colormap = plt.cm.get_cmap(color_map)
    colorlab= 'k'
    coltick = 'k'

    # Sets position of the colorbar
    bw = 0.15 #width of the colorbar
    pad = -0.11#-0.02 #-0.07 # how close is the bar to the plot (negative = closer)
    barsh = 1.0 # height of the bar wrt to the plot


    Nlevels = 50 # Number of colors to use in color map

    # determine the minimum and maximum value in all images
    #minlist = []
    #maxlist = []
    #for x in range(0, len(imnames)): 
    #    img = str(imnames[x])
    #    rapo, depo = RADEC(img)
    #    mn, mx =minmax(img,rapo,depo)
    #    minlist.append(mn)
    #    maxlist.append(mx)
    #mn = min(minlist)
    #mx = max(maxlist)   

    rapo, depo = RADEC(imnames[0]) 

    fig,axs= plt.subplots( 1, len(imnames),figsize=(5*(len(imnames)+0.2),5))

    # find the maximum value in all the mom0 maps
    # this will be used to set a uniform color scale for all images
    allmom0 = []    
    for x in imnames:
        mom0,raarr,decarr,velvec,bmaj,bmin,bpa = calcmom0(x,rapo,depo,svel)
        #mom0max = np.max(mom0)
        allmom0.append(mom0) 


    #pdb.set_trace()
    contmax = np.max(allmom0)  #np.max(allmom0)
    contmin = 0.0
    contvals = np.append(np.arange(contmin, contmax, abs(contmax - contmin)/(Nlevels-1)), contmax)
    contlab = np.append(np.arange(contmin, contmax, abs(contmax - contmin)/(5-1)), contmax)


    add_colorbar = False
    end =len(imnames)-1
    for x in range(0, len(imnames)):
        img =  imnames[x]
        mom0 = allmom0[x]
        #ax = axs[x]
        ax = axs if len(imnames)==1 else axs[x]
        ax.set_title(img)
        #rapo, depo = RADEC(img)
        #mn = min(minlist)
        #mx = max(maxlist)
        print(imnames[end])
        if img == imnames[end]:
            print("True")
            add_colorbar = True
        else: 
            add_colorbar = False
        plotmom0(fig,ax,img,rapo,depo,svel,fts,colormap,colorlab,coltick,\
             bw,pad,barsh,\
             Nlevels,ellicol,\
             window,contvals,contlab,add_colorbar)
    
    print("Moment 0 Maps Generated")
    plt.subplots_adjust(left=0.1,right=0.8)
    plt.show()
    return

#mom0(imnames,svel,color_map,ellipse_color,label_color,window)
