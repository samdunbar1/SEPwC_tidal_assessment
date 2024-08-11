import argparse
import pandas as pd
import datetime
import numpy as np
from matplotlib import dates
from scipy.stats import linregress
import uptide
import pytz


def read_tidal_data(filename):
    """
    Reads in file and removes unnecessary whitespace, rows and missing values to correctly format the file data for analysis

    Args:
    	filename: the data file containing tidal data

    Returns:
    	data: dataframe containing cleaned sea level data with datetime index

    """

# Defines new column names
    column_names = ['Index', 'Date', 'Time', 'Sea Level', 'Residual']

# Reads in file, removes unnecessary whitespace between columns, assigns new column names, skips first 11 rows
    data = pd.read_csv(filename, sep=r'\s+', header=column_names, skiprows=11)

# Combines dates and times into datetime
    date_time = data['Date'] + ' ' + data['Time']
    data['date_time'] = pd.to_datetime(data['data_time'])

# Assigns datetime as the index for thhe data frame
    data = data.set_index('date_time')

# Cleans data by replacing missing/corrupted data with NaN values - From SEPwC Git README
    data.replace(to_replace=".*M$",
                 value={'Sea Level': np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*N$",
                 value={'Sea Level': np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*T$",
                 value={'Sea Level': np.nan}, regex=True, inplace=True)

# Converts sea level data into float
    data['Sea Level'] = data['Sea Level'].astype(float)

    return data


def extract_single_year_remove_mean(year, data):
    """
    Extracts a single year of data from the data frame and removes the mean from the sea level data

    Args:
    	year: the year to be extracted from the data
    	data: tidal data

    Returns:
    	single_year_data: data for the extracted year with mean removed

    """

# Create strings to define the start and end of a given year
    year_start = str(year) + "0101"
    year_end = str(year) + "1231"

# Find the sea level data for a given year in the dataframe
    single_year_data = data.loc[year_start:year_end, ['Sea Level']]

# Calculate the mean of the selected year
    single_year_mean = np.mean(single_year_data['Sea Level'])

# Subtract the mean sea level from the sea level data for the year
    single_year_data['Sea Level'] = single_year_data['Sea Level'] - \
        single_year_mean

    return single_year_data


def extract_section_remove_mean(start, end, data):
    """
    Extracts a specified year from the dataframe and removes the mean from the data

    Args:
    	start: start date for the section
    	end: end date for the data
    	data: path to data file

    Returns:
    	single_section_data:

    """

# Defines the section of data to be read in
    section_start = str(start)
    section_end = str(end)

# Identifies and extracts the specified section of data from the dataframe
    section_data = data.loc[section_start:section_end]

# Calculate mean sea level for the extracted section
    section_mean = np.mean(section_data['Sea Level'])

# Subtract the mean from the sea level data for the section
    section_data['Sea Level'] = section_data['Sea Level'] - section_mean

    return section_data


def join_data(data1, data2):
	"""
    Joins two data files into one combined file and sorts them based on their index.

    Args:
    	data1: First data file to be joined
    	data2: Second data file to be joined

    Returns:
    	joined_data: Sorted file containing the data from the two input files

    """
# Reads in the two data files
	data1 = pd.read_csv(data1)
	data2 = pd.read_csv(data2)

# Concatenates the two data files into one single file
	joined_data = pd.concat([data1, data2])

# Sorts the joined data by the index in ascending order
	joined_data.sort_index(ascending=True, inplace=True)

	return joined_data


def sea_level_rise(data):
    """
    Reads in sea level files and calculates sea level rise using linear regression

	Args:
    	data: tidal data

    Returns:
    	slope: Sea level rise gradient
    	p: p-value
    """

# Drops NaN values from the data
    data = data.dropna(subset=["Sea Level"])

# Converts the index into datetime
    data.index = pd.to_datetime(data.index)

# Assigns data to x and y axis for regression
# Converts datetime into number of days since start
    x_data = dates.date2num(data.index)
    y_data = data["Sea Level"]

# Performs linear regression
    slope, intercept, r, p, se = linregress(x_data, y_data)

    return slope, p


def tidal_analysis(data, constituents, start_datetime):
    
    # Drops unwanted values from Sea Level data
    # Creates tide object for constituents
    data = data.dropna(subset=["Sea Level"])
    tide = uptide.Tides(constituents)

    # Sets the initial time and ensures timezone is correct
    tide.set_initial_time(start_datetime)
    data.index = data.index.tz_localize(None)

    # Converts index into seconds since start of data
    seconds = (data.index - start_datetime).total_second().to_numpy()

    # Conducts harmonic analysis
    amp, pha = uptide.harmonic_analysis(tide, data["Sea Level"], seconds)
    
    return amp, pha


def get_longest_contiguous_data(data):

    """
    Finds the longest stretch of sea level data without encountering any NaN values
    
    Args:
        data: Tidal data
    
    Returns: 
        longest stretch of data without NaN values
        
    """
    
#https://www.youtube.com/watch?v=7Z7x8zleA0w
    data = np.append(np.nan, np.append(data, np.nan))
    
#Locate NaN values in data
    where_null = np.where(np.isnan(data))[0]

#Finds the length of stretches and where the longest is
    longest_contiguous = np.diff(where_null).argmax()
    
#Returns the position of the boundary NaN values
    return where_null[[longest_contiguous, longest_contiguous + 1]]
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Sam Dunbar"
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
    


