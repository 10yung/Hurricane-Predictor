from file_read_backwards import FileReadBackwards
from datetime import *
from pygeodesy import ellipsoidalVincenty as ev
import os
from pathlib import Path



def meter_to_nm(num: float) -> float:
    """
    convert meter to nautical miles (nm)
    :param num: float
    :return: float
    """
    return num / 1852.0

def hour_diff_in_hr(start_date: str, end_date: str) -> float:
    """
    convert string to datetime, and then convert datetime to hour
    :param start_date: str
    :param end_date: str
    :return: float
    """
    start_date = datetime.strptime(start_date,"%Y%m%d%H%M")
    end_date = datetime.strptime(end_date,"%Y%m%d%H%M")
    return (end_date - start_date).seconds / 3600.0


def form_storms_profile(storm_data_dir: str) -> list:
    """
    Create storm profile base on txt file. Read file backward line by line and Use the isalpha to check the block of
    each hurricane. Return storm profile with each hurricane route records
    :param storm_data_dir : str
    :return [{
                'ID': str
                'name': str
                'route': [
                    ['', '', ...],
                    [...],
                    [...],
                    ...
            ]}, {...}, ...]
    """
    storms_profile = []
    storm = {}

    # read line by line from bottom to top with FileReadBackwards package
    with FileReadBackwards(storm_data_dir, encoding="utf-8") as file:
        for line in file:
            # Line start from alpha means finished reading entire storm block
            # append current storm to the storm profile list
            clean_line_list = [item.strip() for item in line.split(',')]

            if line[0].isalpha():

                # get storm name and ID
                storm['ID'] = clean_line_list[0]
                storm['Name'] = clean_line_list[1]

                # append a copy of current storm profile to list and reset parameter
                storms_profile.append(storm.copy())

                # reset storm dictionary using reference
                storm.clear()

            else:
                # create route information in each storm without redundant space
                if 'route' not in storm:
                    storm['route'] = [clean_line_list]
                else:
                    storm['route'].append(clean_line_list)

    return storms_profile


def read_stroms_txt(*file_path: tuple) -> list:
    """
    Read hurricanes from multiple paths and extract each storm information into storm profile summary
    :param file_path:
    :return: storm_profile_summary: List
    """
    storms_profile_summary = []
    for dir in list(file_path):
        storms_profile = form_storms_profile(dir)
        storms_profile_summary = storms_profile_summary + storms_profile

    return storms_profile_summary


def cal_route_dist_time_diff(route: list) -> list:
    """
    calculate each route distance and time firstly, and then calculate the difference of distance and time between each route.

    :param route: list
    :return:[['distance', 'time'], [...], [...], ...]
    """
    route_latlon_time = []

    if (len(route) > 1):
        for i in range(1, len(route)):
            latlon = ev.LatLon(route[i - 1][4], route[i - 1][5])
            latlon_next = ev.LatLon(route[i][4], route[i][5])
            date = route[i - 1][0] + route[i - 1][1]
            date_next = route[i][0] + route[i][1]

            route_latlon_time = route_latlon_time + [[
                meter_to_nm(latlon.distanceTo(latlon_next)),
                hour_diff_in_hr(date, date_next)
            ]]

    else:
        route_latlon_time = [[0.0, 1.0]]

    return route_latlon_time


def find_hurricanes_hitting_location(lat: float, lon: float) -> list:
    """
    Find out those storms will hit the specific location assigned
    :param lat: float
    :param lon: float
    :param storms_profile: list
    :return: ['str', ...]
    """
    dirname = os.path.dirname(__file__)
    dirname = Path(dirname)

    storms_profile = read_stroms_txt(str(dirname.parent)+'/data/atl.txt', str(dirname.parent)+'/data/pac.txt')
    assign_loc = ev.LatLon(lat, lon)
    hit_storm = []

    for storm in storms_profile:
        qualify_storm = False

        for each_route in storm['route']:
            # print(each_route)
            latlon = ev.LatLon(each_route[4], each_route[5])

            if meter_to_nm(latlon.distanceTo(assign_loc)) <= 5.0 and int(each_route[6]) >= 64:
                qualify_storm = True

            quadrant_index = int(latlon.distanceTo3(assign_loc)[-1] // 90)
            quadrant_distance = float(each_route[16:20][quadrant_index])

            if meter_to_nm(quadrant_distance >= latlon.distanceTo(assign_loc)):
                qualify_storm = True

        if qualify_storm == True:
            hit_storm.append(storm['Name'])

    return hit_storm


