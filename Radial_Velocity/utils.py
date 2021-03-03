import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from scipy.optimize import curve_fit as cft
import dfitspy as dft
from astropy.io import fits
import os

def cubic(x, a, b, c, d):
    cc = a + b*x + c*(x**2) + d*(x**3)
    return cc

def line(x, m, c):
    return m*x + c