import pandas as pd
import datetime


def load_data(path):
    '''
    takes the path of the file of interest (str) and returns a pandas dataframe
    '''
    dataframe = pd.read_csv(path, delimiter=',', header=0)
    dataframe['started_at'] = pd.to_datetime(dataframe['started_at'])
    dataframe['ended_at'] = pd.to_datetime(dataframe['ended_at'])
    return dataframe


def hourly_data_by_station(raw_data):
    '''
    takes a pandas dataframe from just eat website as input and returns a dictionary containing a dataframe
    with the mean number of arrivals and departures per hour (averaged over the whole month) for each
    station
    '''
    DFdict = {}

    for station in raw_data.start_station_name.unique():
        # result dataframe containing the number of bikes demanded each day at specified station
        ab_data = raw_data[raw_data['start_station_name'] == station]
        ab_data = ab_data.set_index('started_at')
        ab_data_count = ab_data.resample('H').count()['ended_at']
        ab_data_count_2 = ab_data_count.groupby(ab_data_count.index.hour).mean().reset_index()
        ab_data_count_2.columns = ['hour', 'mean_demand_per_hour']

        # do same for arrivals
        zu_data = raw_data[raw_data['end_station_name'] == station]
        zu_data = zu_data.set_index('ended_at')
        zu_data_count = zu_data.resample('H').count()['started_at']
        zu_data_count_2 = zu_data_count.groupby(zu_data_count.index.hour).mean().reset_index()
        zu_data_count_2.columns = ['hour', 'mean_arrivals_per_hour']

        # join two dataframes
        df_comp = pd.merge(ab_data_count_2, zu_data_count_2, how='outer', on='hour')

        DFdict[station] = df_comp

    return DFdict





