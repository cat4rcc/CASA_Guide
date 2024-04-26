# casaguidebetaready
Claire's CASA Guide Beta Test Ready Version

This Guide is a work in progress. The guide is designed to be an interactive introduction to CASA, Common Astronomy Software Applications Package, which is used to processes data from radio telescopes. 

This repository contains:
- environment.yml  This file has the information to create a python environment capable of running the guide.
- CASAGuideIntro.ipynb
- GuideCleanCont.ipynb
- GuideCleanLine.ipynb
- movie.py
- newmom0.py
- plot_all.py
- plot_cont.py
- Beamsize.py
- movie.gif
- Images Folder, This file contains all of the images that will be displayed in the guide.
- premadeMask

This guide can be launched in mybinder. The environment.yml file will produce the correct environment in mybinder including all dependencies required. This includes numpy, pip, casatasks, and matplotlib.
The jupyter notebooks contain the guide. First the introduction, then the Line Cleaning Guide, and the Continuum Guide. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cat4rcc/casaguidebetaready/HEAD)

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/cat4rcc/casaguidebetaready/HEAD
