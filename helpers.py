#
# Student Name: Rares Popa
# Student ID  : 19159700
#
# helper.py: Helper class which contains all imports and 
#            helper functions used throughout the program
#

import os
import time
import itertools 
import pandas as pd 

import matplotlib.pyplot as plt
import numpy as np
from bokeh.io import output_file, show
from bokeh.plotting import *
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Slider, LabelSet
from datetime import datetime, timedelta
from bokeh.palettes import Dark2_5 as palette
from bokeh.palettes import Category20

#Function which gets file input, checks to make sure 
#no errors and if any errors makes the user reinput the file
def fileInput():
    option=True
    while option:
        csv_file = input("What file are we reading? ") #file name form user
        try:
            #Open and READ the file
            with open(csv_file,'r') as f:
                #read all lines
                fileobj = f.readlines()
                option = None #If no error stop loop
        except OSError as err: #OS error
            print('Error with file open: ', err)
        except: #Other errors
            print('Unexpected error: ', err) 
        
    return fileobj

#Function which gets number input, checks to make sure 
#no errors and if any errors makes the user reinput the number
def numberInput():
    option=True
    while option:
        number = input("> ") #number inputted
        try:
            #Convert number to int
            int(number) 
            option = None #If no error stop loop
        except:
            print('Error: Please input a number')
        
    return number

#It's important to have correct date structure, this function makes
#sure the format is correct and if not returns false, if it is it returns true
def validateDate(date_text):
    try:
        #Check format
        datetime.strptime(date_text, '%d %m %Y %H:%M:%S')
        option = None #If no error stop loop
    except:
        #If error return false
        print("Error: Incorrect data format")
        return False
    return True