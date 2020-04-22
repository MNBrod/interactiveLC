# interactiveLC
## A Python program for the interactive display and manipulation of phase-folded light curves

This program is intended to aid in understanding how raw data extracted from time-series photometry of a periodic object can be turned into phase-folded light curves. This program is not designed to produce carefully formatted outputs or find a specific result, rather it aims to give a visual intuition for what is going on behind the scenes of automated phase-folding.

### Usage
The following outlines a typical workflow for this program.

1. Download this repository
2. Run `python main.py`
3. The program will query you for a few pieces of information: the directory containing the files you want to examine, whether the data in the files is a measurement of flux or magnitude, the name of the column in each .csv file that contains the brightness measurement, and the name of the column that contains the time information. If you have already entered this information in a prior session, instead you will be asked if you want to use the same information, or use new entries.
4. A new CLI will now open up in your terminal, along with a window with three empty plots. Type `scan` to search the given directory for all .csv files. A list of all found files will be displayed, with a number next to each file.
5. Type `open [number]`, where `[number]` is the index of the file you want to examine
6. Type `allplot`. This will populate the plots in the plotting window with three graphs: the raw data, a periodogram, and a phase folded light curve.
7. `allplot` defaults to phase-folding the raw data with the highest peak. To phase fold over a different harmonic of the highest peak, use the `h` command, followed by a number to multiply the peak period by. As an example, typing `h 2` will cause the light curve to be folded over the 2nd harmonic. `h .5` would plot over the 1/2th harmonic.
8. To open/plot a new file, first use the `open` command again, and then call `allplot c`. The `c` tells the program to clear the plots before adding more data.