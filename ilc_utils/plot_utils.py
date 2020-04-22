import lightkurve as lk
import numpy as np 
import matplotlib.pyplot as plt 
from astropy.table import Table
from astropy import units as u


def set_properties(axes, title=None, xlabel=None, ylabel=None):
    if title:
        axes.set_title(title)
    if xlabel:
        axes.set_xlabel(xlabel)
    if ylabel:
        axes.set_ylabel(ylabel)
    return axes

def plot_raw():
    print("unimplemented")

def plot_periodogram(ax, p, highlight=None):
    ax.plot(p.period, p.power)
    if not highlight:
        highlight = p.period_at_max_power.value
    ax.axvline(highlight-.03, linestyle='dashed', color='red')
    ax.axvline(highlight+.03, linestyle='dashed', color='red')
    set_properties(ax, ylabel="Power", xlabel="Period")

def plot_phase_folded(ax, lc, period, epoch, offset=4):    
    t_0_offset = (period / offset) + epoch
    lc.fold(period, t_0_offset).scatter(ax=ax, s=5)
    set_properties(ax, ylabel="Magnitude(ish)")

