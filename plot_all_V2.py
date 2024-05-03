######################################
######################################
#Plot all script - Plots all of the channels contained within an image cube

#Functions: 
#plotall               - Runs all functions contained below
#formax                - Formats the axes
#readingrainbowCASA    - Reads data from the FITS file. Reads out RA, DEC. 
#RADEC                 - Uses Reading rainbow to only extract ra and dec
#plotchans             - Plots all the designated channels in a grid with RA and DEC on the last plot. 

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

#import scipy.io.array_import
from matplotlib.patches import Ellipse
from scipy.ndimage.interpolation import rotate
def plotall(ellicol, img, mask_name, svel, cmap, window, fitsdata, plotMask): 
    
    ############################################################
    def formax(ax,majx,majy,minx,miny):
        majorxLocator   = MultipleLocator(majx)
        majoryLocator   = MultipleLocator(majy)
        majorxFormatter = FormatStrFormatter('%4.0f')
        majoryFormatter = FormatStrFormatter('%4.0f')
        minorxLocator   = MultipleLocator(minx)
        minoryLocator   = MultipleLocator(miny)
        ax.xaxis.set_major_locator(majorxLocator)
        ax.yaxis.set_major_locator(majoryLocator)
        ax.xaxis.set_major_formatter(majorxFormatter)
        ax.yaxis.set_major_formatter(majoryFormatter)
        ax.xaxis.set_minor_locator(minorxLocator)
        ax.yaxis.set_minor_locator(minoryLocator)
        return

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

    def plotchans(fts,colormap,colorlab,coltick,bw,pad,barsh,\
                  Nlevels,nchannels,window,\
                  img,mask_img,svel,rapo,depo, fitsdata):

        flip=False
        data_arr,linefreq,raarr,dearr,dra,bmaj,bmin,bpa,velvec \
            = readingrainbowCASA(img,rapo,depo,nchannels,svel, flip,fitsdata) 
        if plotMask == True:
            mask_arr,maskfreq,maskra,maskde,maskdra,maskbmaj,maskbmin,maskbpa,maskvel = readingrainbowCASA(mask_img,rapo,depo,nchannels,svel,flip,fitsdata=False)

        contmin = data_arr.min()
        contmax = data_arr.max()
        contvals = N.append(N.arange(contmin, contmax, abs(contmax - contmin)/(Nlevels-1)), contmax)
        contlab = N.append(N.arange(contmin, contmax, abs(contmax - contmin)/(5-1)), contmax)

        fig = plt.figure(1,figsize=(11,10)) #change until looks square
        fig.clf()
        ncol =6
        gs0 = gridspec.GridSpec(1,1,left=0.09, right=0.85,top=0.92,bottom=0.1,wspace=0.3,hspace=0.3)
        gs01 = gridspec.GridSpecFromSubplotSpec(7, ncol, subplot_spec=gs0[0])

        nrow = int(nchannels/ncol)
        add_details = (nrow*ncol)-1
        
        for nc in range(nchannels):
            ax = plt.subplot(gs01[nc])
            
            pltarr = data_arr[nc,:,:]  # slice in velocity space

            CS2 = plt.contourf(raarr,dearr,pltarr, levels=contvals, cmap=colormap,extend='both')
            if plotMask == True: 
                pltmask = mask_arr[nc,:,:]
                CSmask = plt.contour(raarr,dearr,pltmask,levels=[1.0],colors='white')

            plt.annotate("%3.1f km/s"%(velvec[nc]), xy=(0.92,0.03), xycoords='axes fraction',
                    color='white', horizontalalignment='right', verticalalignment='bottom',
            fontweight='normal', fontsize=fts-2) #fontname='Bitstream Vera Sans',family='sans-serif')
            formax(ax,6,6,3,3) # this sets number of ticks, major x tick, major y tick, minor x tick, minor y tick
            
            if nc == add_details and fitsdata == True:
                
                plt.ylabel(r"$\Delta\theta_{\rm Dec}''$",fontsize=fts+1,labelpad=3.0)
                plt.xlabel(r"$\Delta\theta_{\rm RA}''$",fontsize=fts+1,labelpad=3.0)
                plt.xticks(rotation=45)
                plt.setp(ax.get_xticklabels(), visible=True)
                plt.setp(ax.get_yticklabels(), visible=True)
                print(bmin, bmaj)
                ellpo = window-1.0 # ellipse position -- center of where the beam will go
                ells = Ellipse(xy=[ellpo,-ellpo], width=bmin*3600.0, height=bmaj*3600.0, angle=bpa*-1,zorder=300)
                ells.set_facecolor(ellicol)
                ells.set_edgecolor(ellicol)
                ax.add_artist(ells)
            else: 
                plt.setp(ax.get_xticklabels(), visible=False)
                plt.setp(ax.get_yticklabels(), visible=False)
                

            ax.set_xlim(window,-1*window)
            ax.set_ylim(-1*window,window)

        # Put the colorbar on the last ax
        pt = ax.get_position().bounds
        cax = fig.add_axes([pt[0]+pt[2]+pad-bw/2, pt[1]+pt[3]*(1.0-barsh)/2.0, bw, pt[3]*barsh])
        cbar = plt.colorbar(CS2, cax=cax, ticks=contlab) #,format=ticker.FuncFormatter(fmt))
        cbar.ax.set_ylabel(r'mJy beam$^{-1}$',fontsize=fts-2,color='k',labelpad=15.0,rotation=270)



        plt.show()
        #fig.savefig('./'+outputname,format="png",dpi=200,transparent=False,bbox_inches='tight',pad_inches=0.1) #bbox_inches='tight',pad_inches=0.1,transparent=True)
        return


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
    nchannels = 30 # number of channels to plot around center of line, +/- nchannels/2

    # increase or decrease to plot more/less of space
   

    outputname = 'out.png'

    #########################################
    #########################################
    #########################################
    img_name = img


    #########################################
    #########################################
    #########################################
    rapo, depo = RADEC(img)
    plotchans(fts,colormap,colorlab,coltick,bw,pad,barsh,\
              Nlevels,nchannels,window,\
              img_name,mask_name,svel,rapo,depo, fitsdata)
    #print(nchannels)
    plt.show()
    return 




