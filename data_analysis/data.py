import pandas as pd
import math
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

    # add new column to each dataframe that contains net flow value

    for station in raw_data.start_station_name.unique():
        single_df = DFdict[station]
        single_df['net_flow_value'] = ''
        for i in range(len(single_df)):
            if i == 0:
                single_df.iloc[i, 3] = single_df.iloc[i, 2] - single_df[i, 1]
            else:
                single_df.iloc[i, 3] = single_df.iloc[i-1, 3] + single_df.iloc[i, 2] - single_df[i, 1]
        DFdict[station] = single_df

    return DFdict

def compute_distance(lat_1, lng_1, lat_2, lng_2):
    '''
    Function calculates the distance between two points, specified through their coordinates
    according to the haversine formula

    Input:
        lat_1, lng_1, lat_2, lng_2 (float): coordinates of the two points between which the
                                            distance shall be calculated (in degrees)
    Output:
        distance (float): distance between the two points in kilometers
    '''
    # convert degrees to radians
    lng_1, lat_1, lng_2, lat_2 = map(math.radians, [lng_1, lat_1, lng_2, lat_2])
    # calculate difference between longitude and latitude coordinates
    dist_lat = lat_2 - lat_1
    dist_lng = lng_2 - lng_1
    # apply haversine formula
    res = (math.sin(dist_lat / 2) ** 2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(dist_lng / 2) ** 2)
    distance = 6373.0 * (2 * math.atan2(math.sqrt(res), math.sqrt(1 - res)))

    return distance




