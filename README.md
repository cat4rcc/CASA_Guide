# CASA Guide: BETA TEST

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cat4rcc/casaguidebetaready/HEAD)

# Claire's CASA Guide Beta Test Ready Version

This Guide is a work in progress.  The guide is designed to be an interactive introduction to CASA, Common Astronomy Software Applications Package, which is used to processes data from radio telescopes.

The CASA Team, et al., *“CASA, the Common Astronomy Software Applications for Radio Astronomy”*, PASP, 134, 114501. DOI: 10.1088/1538-3873/ac9642

# How to Use: 

Before you start: 
Fill out the [Pre-Survey](https://docs.google.com/forms/d/e/1FAIpQLScGCtXByL3see-tT1fMqZQDn-rW3SxwGAAEy3nDJ3jf8Fbniw/viewform?usp=sf_link)

When you are done, please fill out the [Post-Survey](https://docs.google.com/forms/d/e/1FAIpQLSesKg9eb96SLz32fdsoe6cOoh7u8o6yH33n9Mb00h_CtPkg_A/viewform?usp=sf_link)

Download the files and run in your own environment or use mybinder:   [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cat4rcc/casaguidebetaready/HEAD)

This guide can be launched in mybinder. The `Dockerfile.txt` file will produce the correct environment in mybinder.  If you choose to use mybinder, you can launch via the button  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cat4rcc/casaguidebetaready/HEAD) This should set up the correct environment to run CASA. However, the Virtual Machine provided by mybinder, may not be powerful enought to run this guide. It also will not save your progress. 

If you choose to use your own environment, create a new python 3.6 environment and import the files. 

After Launching run the `1_GetData.ipynb` Jupyter Notebook to download the measurements set, images, and premade masks. This file will also install `casatasks`, `casatools`, and other files and packages required to run the guide smoothly. This file will create a lot of outputs! Don't worry if this script produces a red box! 

CASA might be too much for my binder to handle? 

After running the cell in `1_GetData.ipynb`, explore the Introduction in `2_CASAguideIntro.ipynb`, try cleaning the continuum in `3_GuideCleanCont.ipynb`, and then try cleaning the line data in `4_GuideCleanLine.ipynb`! 

Please fill out the [Post-Survey!](https://docs.google.com/forms/d/e/1FAIpQLSesKg9eb96SLz32fdsoe6cOoh7u8o6yH33n9Mb00h_CtPkg_A/viewform?usp=sf_link)



## This repository contains:

| File  | Description  |
| -------- | ------- |
| `DockerFile.txt` | This text file has the information to create a python environment capable of running the guide. This file was created by Aard Keimpema, Tammo Jan Dikema, and Bruno Juncklaus Martins and is available [here](https://github.com/aardk/jupyter-casa) |
| `1_GetData.ipynb` | Installs casatasks, casatools, astropy, and casadata. Downloads and expands the needed Images, Premade Masks and Measurement sets hosted on Box [here](https://virginia.box.com/s/qhc736l24ikriadqvflnf0drhed7ll9z) |
| `2_CASAGuideIntro.ipynb` | An introduction to CASA. Includes: What is a Radio Telescope, What is an Interferometer, Key Parameters for Cleaning Data and More!  |
| `3_GuideCleanCont.ipynb` |  How to Clean Continuum data (Interactive Activity)   |
| `4_GuideCleanLine.ipynb`  | How to Clean Line data (Interactive Activity) |  
| `movie.py` | Makes gif files from set of channel maps generated |
| `newmom0.py` | Makes moment 0 maps  |
| `plot_all.py` | Plots all channels in a grid  |
| `plot_cont.py`  | Plots the continuum  |  
| `Beamsize.py`  | Calculates the size of the beam. Can be used to determine image size |
| `movie.gif` | Sample gif file |
|  Removed for now  `requirements.txt` | This text file contains the required dependencies to run the Guide. This file can be used to generate a python environment will all needed dependencies.   |


# Common Issues 

Images won't load? Run the GetData.ipynb notebook and make sure the Images folder has downloaded. Still not seeing the images? Close the Guide and reopen it. 

File Already Exists: CASA has safety measures not to overwrite existing files. Either remove the pre-existing file or change the name of the file. 

File doesn't exist: There is something wrong with the name of the file CASA is trying to open.  In a new cell, check the name of the file that is being called and check if it is consistent with the files existing in the directory. You can rename the file you want to open or update the name in the script. This is especially if images with 'double' extensions are generated (e.g., 'mask.mask' or '.cont.cont'


