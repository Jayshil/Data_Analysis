import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from scipy.optimize import curve_fit as cft
import dfitspy as dft
from astropy.io import fits
import os
import utils as utl

def order_poly_fit(filename, yorder):
    hdul = fits.open(filename)
    h11 = hdul[2].data
    h22 = np.transpose(h11)
    data_order = h22[yorder:yorder+50]
    points = np.arange(50, 4000, 30)
    maximum = np.array([])
    for i in range(len(points)):
        d11 = data_order[:, points[i]]
        maxi = np.max(d11)
        bb = np.where(d11 == maxi)
        maximum = np.hstack((maximum, bb[0]))
    popt, pcov = cft(utl.cubic, points, maximum)
    return popt