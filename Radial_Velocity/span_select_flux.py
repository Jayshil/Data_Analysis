import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import os
from pathlib import Path
from astropy.nddata import CCDData
import ccdproc as ccdp
from astropy.stats import mad_std
import utils as utl
import astropy.units as u
import shutil
from scipy.optimize import minimize as mz
from scipy.optimize import curve_fit as cft

def selection(loc, flux_file):
    # Reading the data
    pix, fl, fle = np.loadtxt(loc + flux_file, usecols=(0,1,2), unpack=True)
    # ---------------------------------------
    # To select the region of spectral lines
    # ---------------------------------------
    selection = []
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(211)

    ax.errorbar(pix, fl, yerr=fle)
    ax.grid()
    #ax.set_ylim(-2, 2)
    ax.set_title('Press left mouse button and drag to select the region of the spectrum you want to mask. (You can use zoom button to see the minor features)')

    ax2 = fig.add_subplot(212)
    line2, = ax2.plot(pix, fl, '-')
    ax2.grid()

    def onselect(xmin, xmax):
        indmin, indmax = np.searchsorted(pix, (xmin, xmax))
        indmax = min(len(pix) - 1, indmax)

        thisx = pix[indmin:indmax]
        thisy = fl[indmin:indmax]
        line2.set_data(thisx, thisy)
        ax2.set_xlim(thisx[0], thisx[-1])
        ax2.set_ylim(thisy.min(), thisy.max())
        ax2.grid()
        fig.canvas.draw_idle()
        ab = [indmin, indmax]
        selection.append(ab)

    # set useblit True on gtkagg for enhanced performance
    span = SpanSelector(ax, onselect, 'horizontal', useblit=True, 
                         rectprops=dict(alpha=0.5, facecolor='red'))
    plt.show()

    mid_pix = []
    mid_pix_err = []

    for i in range(len(selection)):
        aa = int(selection[i][0])
        bb = int(selection[i][1])
        pix1 = pix[aa:bb]
        fl1 = fl[aa:bb]
        fle1 = fle[aa:bb]
        #xinit = np.array([fl1[0], 1, 1, 1])
        #"""
        mini = np.min(fl1)
        mini1 = np.where(fl1 == mini)
        #mid_pix.append(pix1[mini1[0][0]])
        #"""
        xinit = np.array([pix1[mini1[0][0]], pix1[-1]-pix1[0], fl1[0], 1])
        #xinit = np.array([(pix1[0] + pix1[-1])/2, pix1[-1]-pix1[0], fl1[5], 1])
        def min_log_likelihood(x):
            #model = utl.cubic(pix1, x[0], x[1], x[2], x[3])
            model = utl.neg_gaus(pix1, x[0], x[1], x[2], x[3])
            chi2 = (fl1 - model)/fle1
            chi22 = np.sum(chi2**2)
            yy = np.sum(np.log(fle1)) + 0.5*chi22
            return yy
        soln = mz(min_log_likelihood, xinit, method='BFGS')
        covMat=2*soln.hess_inv
        mid_pix.append(soln.x[0])
        mid_pix_err.append(covMat[0][0])
        plt.errorbar(pix, fl, yerr=fle, color='orangered', alpha=0.3, zorder=1)
        plt.plot(pix, utl.neg_gaus(pix, soln.x[0], soln.x[1], soln.x[2], soln.x[3]), 'k-', zorder=i+2)
    plt.grid()
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.show()
    return mid_pix, mid_pix_err

p22 = os.getcwd() + '/Radial_Velocity/Results/'

list1 = os.listdir(p22)
list2 = []

for i in range(len(list1)):
    if list1[i][-12:] == '_spectra.dat':
        list2.append(list1[i])

list2.sort(key=utl.natural_keys)

f22 = open(p22 + 'positions_4_n2.dat', 'w')
f33 = open(p22 + 'positions_4_err_n2.dat', 'w')
list3 = [list2[13]]

for j in range(len(list3)):
    mid_pix1, mid_pix2 = selection(p22, list3[j])
    if len(mid_pix1) == 0:
        break
    for k in range(len(mid_pix1)):
        f22.write(str(mid_pix1[k]) + '\t')
        f33.write(str(mid_pix2[k]) + '\t')
    f22.write('\n')
    f33.write('\n')

f22.close()
f33.close()