import os
import importlib
import pickle
import numpy as np
from pathlib import Path

from astropy.table import Table

def query_user_for_initial_arguments():
    if os.path.exists("interactive_lc.init"):
        inp = input("Read from previous session? (y/n) ")
        while (inp != "y" and inp != "n"):
            print("Please enter (y/n)")
            inp = input("Read from previous session? (y/n) ")
        if inp == "y":
            with open("interactive_lc.init", 'rb') as h:
                return pickle.load(h)
    file_in_mag = False
    inp = input("Directory containing data files: ")
    try:
        directory = Path(str(inp))
    except:
        print("Error accessing input directory")
    inp = input("Does the data file contain fluxes or magnitudes? (f/m, default f) " )
    while ((inp != 'f') and (inp != 'm') and (inp != 'F') and (inp != 'M')):
        inp = input("Please enter valid input (f/m): ")
    if inp == "m":
        file_in_mag = True
    inp = input("Enter " + ("Flux" if not file_in_mag else "Magnitude") + " column name: (default \"flux\") ")
    input_column_name = str(inp)
    if input_column_name == "":
        input_column_name = "flux"
    inp = input("Enter time column name: (default \"hjd\") ")
    time_column_name = str(inp)
    if time_column_name == "":
        time_column_name = "hjd"
    output = {
        "directory" : directory,
        "data_in_flux" : not file_in_mag,
        "data_col_name" : input_column_name,
        "time_col_name" : time_column_name
    }
    with open("interactive_lc.init", 'wb') as h:
        pickle.dump(output, h)
    return output

def open_data_file(filepath, filename, data_column_name, time_column_name):
    try:
        t = Table.read(filepath / filename)
        try:
            data = t[data_column_name]
        except:
            raise ValueError("Invalid Data Column Name: " + str(data_column_name))
        try:
            time = t[time_column_name]
        except:
            raise ValueError("Invalid Time Column Name: " + str(time_column_name))
        return np.array(time), np.array(data)
    except:
        raise ValueError("Invalid file location: " + str(filepath))

def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def set_color(c):
    if (not is_int(c)):
        raise TypeError
    os.system('color ' + str(c))