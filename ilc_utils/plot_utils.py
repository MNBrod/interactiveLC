import lightkurve as lk
import numpy as np 
import matplotlib.pyplot as plt 
from astropy.table import Table
from astropy import units as u


def set_properties(axes, title=None, xlabel=None, ylabel=None):
    '''
    Sets the title, xlabel, and ylabel atributes of the given axes

    Parameters
    -------
    axes: matplotlib axes object
        The axes to be modified
    title: str
        The title to be added. If none, no title is added
    xlabel: str
        The label to be added. If none, no label is added
    ylabel: str
        The label to be added. If none, no label is added
    '''
    if title:
        axes.set_title(title)
    if xlabel:
        axes.set_xlabel(xlabel)
    if ylabel:
        axes.set_ylabel(ylabel)
    return axes

def plot_periodogram(ax, p, highlight=None):
    '''
    Plots a periodogram from a lightkurve.Periodogram object to the given axes

    Parameters
    -------
    ax: matplotlib axes object
        The axes to be plotted onto
    p: lightkurve Periodogram
        The periodogram to be plotted
    highlight: astropy Time
        The period to highlight on the plot. If none is given, defaults to
        highlighting the highest peak
    '''
    ax.plot(p.period, p.power)
    if not highlight:
        highlight = p.period_at_max_power.value
    ax.axvline(highlight-.03, linestyle='dashed', color='red')
    ax.axvline(highlight+.03, linestyle='dashed', color='red')
    set_properties(ax, ylabel="Power", xlabel="Period")

def plot_phase_folded(ax, lc, period, epoch, offset=4):
    '''
    Plots a phase-folded light curve onto the given axes

    Parameters
    -------
    ax: matplotlib axes object
        The axes to be plotted onto
    lc: lightkurve LightCurve
        The light curve to phase fold and then plot
    period: astropy Time
        The period to phase-fold over
    epoch: astropy Time
        Epoch to use when phase folding
    offset: int
        Inverse fractional component to offset the lightcurve by. For example,
        the default value of 4 will offset the primary eclipse by 1/4 of a
        period to the left, so that both eclipses are visible
    '''    
    t_0_offset = (period / offset) + epoch
    lc.fold(period, t_0_offset).scatter(ax=ax, s=5)
    set_properties(ax, ylabel="Magnitude(ish)")

