#!/usr/bin/env python3

# import the modules you need here
import argparse
import pandas as pd
import datetime
import numpy as np

def read_tidal_data(filename):
    
    """Reads in a file and removes unnecessary whitespace, rows and missing values to correctly format the file data for analysis."""
    
    #Defines new column names
    column_names = ['Index', 'Date', 'Time', 'Sea Level', 'Residual']
    
    #Reads in file, removes unnecessary whitespace between columns, assigns new column names, skips first 11 rows
    dataframe = pd.read_csv(filename, sep = r'\s+', header = column_names, skiprows = 11)
    
    #Combines dates and times into datetime
    date_time = dataframe['Date'] + ' ' + dataframe['Time']
    dataframe['date_time'] = pd.to_datetime(dataframe['data_time'])
    
    #Assigns datetime as the index for thhe data frame
    dataframe = dataframe.set_index('date_time')

    #Cleans data by replacing missing/corrupted data with NaN values - From SEPwC Git README
    dataframe.replace(to_replace=".*M$",value={'Sea Level':np.nan},regex=True,inplace=True)
    dataframe.replace(to_replace=".*N$",value={'Sea Level':np.nan},regex=True,inplace=True)
    dataframe.replace(to_replace=".*T$",value={'Sea Level':np.nan},regex=True,inplace=True)
    
    #Converts sea level data into float
    dataframe['Sea Level'] = dataframe['Sea Level'].astype(float)
    
    return dataframe
   
   
def extract_single_year_remove_mean(year, data):
    
    #Create strings to define the start and end of a given year
    year_start = str(year) + "01-01"
    year_end = str(year) + "12-31"
    
    #Find the sea level data for a given year in the dataframe
    single_year_data = dataframe.loc[year_start:year_end, ['Sea Level']]
    
    #Calculate the mean of the selected year
    single_year_mean = np.mean(single_year_data['Sea Level'])
    
    #Subtract the mean sea level from the sea level data for the year
    single_year_data['Sea Level'] = single_year_data['Sea Level'] - single_year_mean
    
    return single_year_data


def extract_section_remove_mean(start, end, data):


    return 


def join_data(data1, data2):

    return 



def sea_level_rise(data):

                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):


    return 

def get_longest_contiguous_data(data):


    return 

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Jon Hill"
                     )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose
    


