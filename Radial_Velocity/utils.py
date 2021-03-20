import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from scipy.optimize import curve_fit as cft
import dfitspy as dft
from astropy.io import fits
import os
import re

#------------------------------------------------------------------
#---------------------Basic Polynomials----------------------------
#------------------------------------------------------------------

def cubic(x, a, b, c, d):
    cc = a + b*x + c*(x**2) + d*(x**3)
    return cc

def line(x, m, c):
    return m*x + c

def cubic_104(x, a, b, c, d):
    cc = a + b*x + c*(x**2) + d*(x**3)
    return cc + 725

#------------------------------------------------------------------------------------------
#-------------------------------Natural Sorting--------------------------------------------
#------------------------------------------------------------------------------------------
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


#------------------------------------------------------------------
#---------------------Negative Gaussian----------------------------
#------------------------------------------------------------------

def neg_gaus(x, mu, sig, const, aa):
    yy = np.exp(-0.5*((x-mu)/sig)**2)
    zz = -aa*yy + const
    return zz

def neg_gaus1(x, mu, sig, aa):
    yy = np.exp(-0.5*((x-mu)/sig)**2)
    zz = -aa*yy
    return zz

def gaus(x, mu, sig, const, aa):
    yy = np.exp(-0.5*((x-mu)/sig)**2)
    zz = aa*yy + const
    return zz

#------------------------------------------------------------------
#-----------------Wavelength Calibration---------------------------
#------------------------------------------------------------------

def wave_from_pix(pix):
    """
    To compute wavelength from pixel space
    --------------------------------------
    Parameters:
    -----------
    pix : float, numpy.ndarray
        pixel space
    -----------
    return
    -----------
    float, numpy.ndarray
        wavelength
    """
    popt5 = np.array([5.85186740e+03, 1.87472777e-02, -6.43063727e-07, -5.82399577e-13])
    wave2 = cubic(pix, *popt5)
    return wave2
    