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

def selection(flux, error_flx):
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
    return selection