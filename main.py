import importlib
from pathlib import Path
from cmd import Cmd

from ilc_utils import CLI_utilities
from ilc_utils import plot_utils

import numpy as np
import matplotlib.pyplot as plt
import lightkurve as lk

plt.ion()

params = CLI_utilities.query_user_for_initial_arguments()

class lc_prompt(Cmd):

    # Cmd instance variables
    prompt = 'lc> '
    intro = "Welcome! Type intro to get a quick guide to how to use this program. \nType ? to list commands"
    
    # I/O
    files = []
    openned = False
    output = ["ID, Period (d), Epoch (HJD)"]

    # Current LC info
    name = None
    data = None
    time = None
    period = None
    epoch = None
    min_t = .5
    max_t = 3
    freq = 1000

    def __init__(self):
        Cmd.__init__(self)

        # Set up the axes for plotting
        self.fig, self.axes = plt.subplots(3,figsize=(8,10))
        

    # --- File Handling

    def do_open(self, inp):
        print("opening '{}'".format(inp))
        if (CLI_utilities.is_int(inp)):
            if self.files:
                print("Filename: " + self.files[int(inp)].stem)
                inp = self.files[int(inp)]
            else:
                print("Please scan a directory before accessing files by index")
                return
        try:
            t, d = CLI_utilities.open_data_file(params['directory'], inp, params['data_col_name'], params['time_col_name'])
            if not params['data_in_flux']:
                mag = (np.max(d) - d) + 10
                self.data = mag
            else:
                self.data = d
            self.time = t
            self.initialize_lightkurve()
            self.name = inp.stem    
            self.openned = True
            self.fig.suptitle(inp.stem)    
        except:
            print("Error opening " + str(inp))

    def help_open(self):
        print("Load a new data file into the current file buffer.")
        print("If a directory has been scanned, then you may access images by index")
    
    def do_scan(self, inp):
        suffix = '.csv'
        if inp:
            suffix = str(inp)
        fs = [e for e in params['directory'].iterdir() if e.suffix == suffix]
        print("Found the following " + suffix + " files:")
        i = 0
        for n in fs:
            print("(" + str(i) + ") --- " + n.stem)
            i = i + 1
        self.files = fs

    def help_scan(self):
        print("Scans the directory given in the initialization for .csv files.")

    # --- Plotting

    def do_splot(self, inp):
        ax = self.axes[0]
        if (not self.openned):
            print("Please load a light curve before attempting to plot")
            return
        if (inp == 'c'):
            ax.clear()
        ax.scatter(self.time, self.data)
        plot_utils.set_properties(ax, xlabel=params['time_col_name'], ylabel="Flux" if params['data_in_flux'] else "Magnitude")
        plt.draw()

    def help_splot(self):
        print("Plots the raw data of the current Light Curve")
        print("Options:")
        print("   [c] --- clear this plot before adding new data")

    def do_pplot(self, inp):
        ax = self.axes[1]
        if (not self.openned):
            print("Please load a light curve before attempting to plot")
            return
        if (inp == 'c'):
            ax.clear()
        p = self.get_periodogram()
        plot_utils.plot_periodogram(ax, p)
        self.period = p.period_at_max_power
        self.epoch = p.transit_time_at_max_power
        plt.draw()
    
    def help_pplot(self):
        print("Plots a periodogram of the current light curve")
        print("Options:")
        print("   [c] --- clear this plot before adding new data")
    
    def do_fplot(self, inp):
        ax = self.axes[2]
        if (not self.openned):
            print("Please load a light curve before attempting to plot")
            return
        if (inp == 'c'):
            ax.clear()
        p = self.get_periodogram()
        plot_utils.plot_phase_folded(ax, self.lc, p.period_at_max_power.value, (p.transit_time_at_max_power + self.time[0]))

    def help_fplot(self):
        print("Plots a phase-folded version of the current light curve")
        print("Options:")
        print("   [c] --- clear this plot before adding new data")
    
    def do_allplot(self, inp):
        self.do_splot(inp)
        self.do_pplot(inp)
        self.do_fplot(inp)
    
    def help_allplot(self):
        print("Plots all three figures with the current light curve")
        print("Options:")
        print("   [c] --- clear this plot before adding new data")

    # --- Plot Manipulation

    def do_h(self, inp):
        if (not self.openned):
            print("Please load a light curve before attempting to plot")
            return
        
        self.axes[1].clear()
        p = self.get_periodogram()
        max_p =p.period_at_max_power.value
        new_p = max_p * float(inp)

        plot_utils.plot_periodogram(self.axes[1], p, highlight=new_p)

        self.axes[2].clear()
        plot_utils.plot_phase_folded(self.axes[2], self.lc, new_p, p.transit_time_at_max_power)

        plt.draw()

        self.period = new_p
    
    def help_h(self):
        print("Selects the given harmonic as the period to phase-fold over")
        print("Options:")
        print("   [value] --- This number is multiplied with the maximum period from the BLS. For example, an entry of [2] would double the period. A value of [.5] would half it.") 

    def do_mint(self, inp):
        if CLI_utilities.is_int(inp):
            self.min_t = float(inp)
        else:
            print("Please enter a float")

    def help_mint(self):
        print("Change the lower bound on the periods used in the periodogram. Setting this value below .5 can result in errors (default is .5)")

    def do_maxt(self, inp):
        if CLI_utilities.is_float(inp):
            self.max_t = float(inp)
        else:
            print("Please enter a float")
        
    def help_maxt(self):
        print ("Change the upper bound on the periods used in the periodogram (default is three days)")
    
    # --- Output

    def do_scp(self, inp):
        print("Period: " + str(self.period))
        print("Epoch: " + str(self.epoch + self.time[0]))
        self.output.append(str(self.name) + ", " + str(self.period) + ", " + str(self.epoch + self.time[0]))

    def help_scp(self):
        print("Save the current period and epoch to the output list")

    def do_printout(self, inp):
        for i in self.output:
            print(i)
    
    def help_printout(self):
        print("Prints all of the saved output up to this point.")
    
    # --- Informational

    def do_printfiles(self, inp):
        i = 0
        for n in self.files:
            print("(" + str(i) + ") --- " + n.stem)
            i = i + 1
    
    def help_printfiles(self):
        print("Prints all files that have been found with [scan]")

    def do_printinit(self, inp):
        print(params)

    def help_printinit(self):
        print("Prints the values given in the initilization")

    def do_intro(self, inp):
        print("First, you need to open a file to look at. This can be done in two ways:")
        print("   Call 'open [filename]' to open a specific file by name")
        print("   Call 'scan' to search the directory specified on startup for .csv files,\n   and then call 'open [index]', where [index] is the number displayed next to\n   the file you want")
        print("Call 'allplot' to plot the raw data, a periodogram, and a phase-folded LC wit\n the phase extracted from the periodogram")
        print("Call 'h [number]', where [number] is the harmonic of the maximum peak you want\n to phase fold over")
        print("Open a new file, and call 'allplot c' (the c specifies that you want to clear\nthe old plot")
    
    # --- command line specific
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        print("Default: {}".format(inp))

    def do_exit(self, inp):
        plt.close()
        print("closing...")
        CLI_utilities.set_color(7)
        CLI_utilities.cls()
        return True
    
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    
    def preloop(self):
        CLI_utilities.cls()
        CLI_utilities.set_color(3)

    # --- Non-Cmd functions

    def initialize_lightkurve(self):
        self.lc = lk.LightCurve(time=self.time, flux=self.data)

    def get_periodogram(self):
        return self.lc.to_periodogram(method='bls', minimum_period=self.min_t, maximum_period=self.max_t, frequency_factor=self.freq)
 
if __name__ == '__main__':
    lc_prompt().cmdloop()
