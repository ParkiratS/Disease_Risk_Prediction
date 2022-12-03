from opencage.geocoder import OpenCageGeocode
import requests
import math
import random

important_info = {'Gmaps_api_key' : "AIzaSyBwVPcm0csBOu_qgM0P4ruhXihSNojUF8I",  'Geocode_api_key':'ccd8c35096e64bff9360bd9ef7a82032', 'GmapsURL' : "https://maps.googleapis.com/maps/api/staticmap?"}
num_of_images = [10,8]
city_name = input('Please type in the city you would like to see: ')



def get_GEO_Location(location):
    geocoder = OpenCageGeocode(important_info['Geocode_api_key'])
    results = geocoder.geocode(location)
    return (results[0]['geometry']['lat'] , results[0]['geometry']['lng'])

city_center_coords = get_GEO_Location(city_name)
lat_oneMile_Degree = 1/69
long_oneMile_Degree = 1/(math.cos(city_center_coords[0]*(math.pi/180))*69.1710411)

def get_topLeft_corner():
    topLeft_lat = city_center_coords[0] + (num_of_images[0]/2)*lat_oneMile_Degree
    topLeft_long = city_center_coords[1] - (num_of_images[1]/2)*long_oneMile_Degree
    return (topLeft_lat, topLeft_long)
    


topLeft_coords = get_topLeft_corner()
city_grid_coords = []


def get_zoom_in_coords():
    current_coords = list(topLeft_coords)
    for lat_Mile in range(num_of_images[0]):
        for long_Mile in range(num_of_images[1]):
            new_long_coord = current_coords[1]+(random.random()*long_oneMile_Degree)
            new_lat_coord = current_coords[0]+(random.random()*lat_oneMile_Degree)
            city_grid_coords.append((new_lat_coord,new_long_coord))
            current_coords[1] = current_coords[1]+long_oneMile_Degree
        
        current_coords[0] = current_coords[0]-lat_oneMile_Degree
        current_coords[1] = topLeft_coords[1]


    


def get_sat_pics(zoom):
    get_zoom_in_coords()
    for index, coord in enumerate(city_grid_coords):
        r = requests.get(important_info['GmapsURL'] + 'center=' +str(coord[0]) + ',' + str(coord[1]) + '&zoom=' + str(zoom) + '&size=1000x1000&maptype=satellite&format=png8&key='+important_info['Gmaps_api_key'])    
        with open('Images/test' +str(index)+ '.png', 'wb') as file:
            print('Getting image: ' + str(index+1) + ',' + str(coord))
            file.write(r.content)

get_sat_pics(19)