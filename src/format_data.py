#!/usr/bin/python3

"""
    This file contains functions that format data to convert time-of-change
    data to data acquired at fixed intervals

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/04/11
"""

# import python internal libraries
from datetime import datetime, timedelta

# import third party libraries
from pandas import DataFrame

# import user-defined libraries


# write functions
def convert_df(datadf: DataFrame, start_time: datetime,
               interval: float=600, step: bool=True) -> DataFrame:
    """
        This function converts a dataframe which data are converted according
        to time of change of values to data collected at fixed intervals.
        Return a pandas DataFrame collected at fixed intervals

        Inputs:
        ==========
        datadf: pandas DataFrame
            dataframe which index are datetime.datetime objects and contain
            data collected at time of change

        start_time: datetime.datetime
            user-defined starting time

        interval: float
            user-defined time interval for the new data frame in seconds.
            Default 600 (10 minutes)

        step: bool
            if the data should be considered to be step functions. Default
            True. Indeed this input won't work until further notice.
    """

    # calculate the ending index for the new dataframe
    num = 1
    while start_time+timedelta(seconds=interval*num) < datadf.index[-1]:
        num += 1
    end_time = start_time+timedelta(seconds=interval*(num-1))

    # create the new dataframe with the correct indexes and column names
    final_df = DataFrame(index=[
        start_time+timedelta(seconds=interval*ind) for ind in range(num)
    ], columns=datadf.columns)

    if step:
        # calculate the starting values for the new dataframe

        # continue to append new columns until the end

        pass
    else:
        raise ValueError(u''.join([
            u'The interpolation function of format_data.convert_df is',
            u' incomplete. Should not be used for now.'
        ]))

    return final_df


# testing functions
if __name__ == '__main__':

    from os.path import basename
    from data_read import read_data

    FILENAME = '../dat/time_of_change.csv'
    TEST_DF = read_data(FILENAME, header=0)
    NEW_DF = convert_df(TEST_DF, datetime(2011, 1, 11, 0, 0))
    assert isinstance(NEW_DF, DataFrame)
    assert NEW_DF.index[-1] <= TEST_DF.index[-1]
    assert NEW_DF.index[-1] >= TEST_DF.index[-2]

    print('All functions in', basename(__file__), 'are ok')