import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from scipy.optimize import curve_fit as cft
import dfitspy as dft
from astropy.io import fits
import os
import re

def cubic(x, a, b, c, d):
    cc = a + b*x + c*(x**2) + d*(x**3)
    return cc

def line(x, m, c):
    return m*x + c

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
