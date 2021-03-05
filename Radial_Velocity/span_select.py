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