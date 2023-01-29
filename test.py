from opencage.geocoder import OpenCageGeocode
import requests
import math
import random
import numpy as np
import imageio
from io import BytesIO
import matplotlib.pyplot as plt
from bruh import complete_Model

from tqdm import tqdm

def tonp(c): return imageio.imread(BytesIO(c))
important_info = {'Gmaps_api_key' : "AIzaSyBwVPcm0csBOu_qgM0P4ruhXihSNojUF8I",  'Geocode_api_key':'ccd8c35096e64bff9360bd9ef7a82032', 'GmapsURL' : "https://maps.googleapis.com/maps/api/staticmap?"}
num_of_images = [20,20]
city_name = input('Please type in the city you would like to see: ')
ims_to_train = []
ims_to_show = []


def get_GEO_Location(location):
    geocoder = OpenCageGeocode(important_info['Geocode_api_key'])
    results = geocoder.geocode(location)
    return (results[0]['geometry']['lat'] , results[0]['geometry']['lng'])

city_center_coords = get_GEO_Location(city_name)
lat_oneMile_Degree = (1/69)*0.11
long_oneMile_Degree = (1/(math.cos(city_center_coords[0]*(math.pi/180))*69.1710411))*0.1

def get_topLeft_corner():
    topLeft_lat = city_center_coords[0] + (num_of_images[0]/2)*lat_oneMile_Degree
    topLeft_long = city_center_coords[1] - (num_of_images[1]/2)*long_oneMile_Degree
    return (topLeft_lat, topLeft_long)
    


topLeft_coords = get_topLeft_corner()
city_grid_coords = []


def get_zoom_in_coords():
    current_coords = list(topLeft_coords)
    for lat_Mile in range(num_of_images[0]):
        ims_to_show.append([])
        ims_to_train.append([])
        for long_Mile in range(num_of_images[1]):
            new_long_coord = current_coords[1]#+(random.random()*long_oneMile_Degree)
            new_lat_coord = current_coords[0]#+(random.random()*lat_oneMile_Degree)
            city_grid_coords.append((new_lat_coord,new_long_coord))
            current_coords[1] = current_coords[1]+long_oneMile_Degree
        
        current_coords[0] = current_coords[0]-lat_oneMile_Degree
        current_coords[1] = topLeft_coords[1]


def get_sat_pics(zoom):
    get_zoom_in_coords()
    for index, coord in tqdm(enumerate(city_grid_coords)):
        r = requests.get(important_info['GmapsURL'] + 'center=' +str(coord[0]) + ',' + str(coord[1]) + '&zoom=' + str(zoom) + '&size=1000x1000&maptype=satellite&format=png8&key='+important_info['Gmaps_api_key'])    
        with open('Images/test' +str(index)+ '.png', 'wb') as file:
            ims_to_show[int(index/num_of_images[0])].append(tonp(r.content)[:620])
            ims_to_train[(int(index/num_of_images[0]))].append(tonp(r.content))
            file.write(r.content)

def create_Heat_Map():
    HM = []

    for i in range(len(ims_to_train)):
        HM.append([])
        for j in tqdm(range(len(ims_to_train[i]))):
            IMG = ims_to_train[i,j:j+1,:,:,:3]
            PRED = model.predict(IMG)
            INDUSTRIAL = PRED[0,0]*0.515
            RICH = PRED[0,1]*85
            SLUMS = PRED[0,2]*0.33
            RED = SLUMS
            GREEN = RICH
            BLUE = INDUSTRIAL


            RGB = [RED, GREEN, BLUE]
            HM[i].append(RGB)
    cleanRGB(HM)
    return np.array(HM)

def cleanRGB(arr):
    for r in range(len(arr)):
        for c in range(len(arr[r])): 
            if r == 0:
                if c == 0:
                    arr[r][c][0] = (arr[r][c+1][0] + arr[r+1][c][0] + arr[r][c][0])/3
                    arr[r][c][1] = (arr[r][c+1][1] + arr[r+1][c][1] + arr[r][c][1])/3
                    arr[r][c][2] = (arr[r][c+1][2] + arr[r+1][c][2] + arr[r][c][2])/3
                elif c == num_of_images[1]-1:
                    arr[r][c][0] = (arr[r][c-1][0] + arr[r+1][c][0] + arr[r][c][0])/3
                    arr[r][c][1] = (arr[r][c-1][1] + arr[r+1][c][1] + arr[r][c][1])/3
                    arr[r][c][2] = (arr[r][c-1][2] + arr[r+1][c][2] + arr[r][c][2])/3
                else:
                    arr[r][c][0] = (arr[r][c+1][0]+ arr[r][c-1][0] + arr[r+1][c][0] + arr[r][c][0])/4
                    arr[r][c][1] = (arr[r][c+1][1]+ arr[r][c-1][1] + arr[r+1][c][1] + arr[r][c][1])/4
                    arr[r][c][2] = (arr[r][c+1][1]+ arr[r][c-1][1] + arr[r+1][c][1] + arr[r][c][1])/4

            elif r == num_of_images[0]-1:

                if c == 0:
                    arr[r][c][0] = (arr[r][c+1][0] + arr[r-1][c][0] + arr[r][c][0])/3
                    arr[r][c][1] = (arr[r][c+1][1] + arr[r-1][c][1] + arr[r][c][1])/3
                    arr[r][c][2] = (arr[r][c+1][2] + arr[r-1][c][2] + arr[r][c][2])/3
                elif c == num_of_images[1]-1:
                    arr[r][c][0] = (arr[r][c-1][0] + arr[r-1][c][0] + arr[r][c][0])/3
                    arr[r][c][1] = (arr[r][c-1][1] + arr[r-1][c][1] + arr[r][c][1])/3
                    arr[r][c][2] = (arr[r][c-1][2] + arr[r-1][c][2] + arr[r][c][2])/3
                else:
                    arr[r][c][0] = (arr[r][c+1][0]+ arr[r][c-1][0] + arr[r-1][c][0] + arr[r][c][0])/4
                    arr[r][c][1] = (arr[r][c+1][1]+ arr[r][c-1][1] + arr[r-1][c][1] + arr[r][c][1])/4
                    arr[r][c][2] = (arr[r][c+1][1]+ arr[r][c-1][1] + arr[r-1][c][1] + arr[r][c][1])/4
            elif c == 0:
                arr[r][c][0] = (arr[r][c+1][0] + arr[r-1][c][0]+arr[r+1][c][0] + arr[r][c][0])/4
                arr[r][c][1] = (arr[r][c+1][1] + arr[r-1][c][1]+arr[r+1][c][1] + arr[r][c][1])/4
                arr[r][c][2] = (arr[r][c+1][2] + arr[r-1][c][2]+arr[r+1][c][2] + arr[r][c][2])/4
            
            elif c == num_of_images[1]-1:
                arr[r][c][0] = (arr[r][c-1][0] + arr[r-1][c][0]+arr[r+1][c][0] + arr[r][c][0])/4
                arr[r][c][1] = (arr[r][c-1][1] + arr[r-1][c][1]+arr[r+1][c][1] + arr[r][c][1])/4
                arr[r][c][2] = (arr[r][c-1][2] + arr[r-1][c][2]+arr[r+1][c][2] + arr[r][c][2])/4
            else:
                arr[r][c][0] = (arr[r][c+1][0]+ arr[r][c-1][0] + arr[r-1][c][0]+arr[r+1][c][0] + arr[r][c][0])/5
                arr[r][c][1] = (arr[r][c+1][1]+ arr[r][c-1][1] + arr[r-1][c][1]+arr[r+1][c][1] + arr[r][c][1])/5
                arr[r][c][2] = (arr[r][c+1][2]+ arr[r][c-1][2] + arr[r-1][c][2]+arr[r+1][c][2] + arr[r][c][2])/5
    

    for r in arr:
        for c in r:
            if (c[0] > c[1]) and (c[0] > c[2]):
                c[1] = c[1]*0.5
                c[2] = c[2]*0.5

            elif (c[1] > c[2]) and (c[1] > c[0]):
                c[0] = c[0]*0.5
                c[2] = c[2]*0.5

            else:
                c[0] = c[0]*0.5
                c[1] = c[1]*0.5
    



get_sat_pics(19)
ims_to_show = np.array(ims_to_show)
im = np.hstack([np.vstack(ims_to_show[:,i]) for i in range(num_of_images[0]-1)])
plt.imshow(im)
plt.show()

model = complete_Model()
ims_to_train = np.array(ims_to_train)
heat_map = create_Heat_Map()

plt.imshow(heat_map, alpha = 0.8)
plt.show()
# a = 0.11
# b = 0.095

# from tqdm import tqdm

# def cos(deg):
#   return np.cos(deg*np.pi/180.)

# n = 3

# ims = [[None for i in range(2*n-1)] for j in range(2*n-1)]

# def getimg(coord, zoom, index):
#   r = requests.get(important_info['GmapsURL'] + 'center=' +str(coord[0]) + ',' + str(coord[1]) + '&zoom=' + str(zoom) + '&size=1000x1000&maptype=satellite&format=png8&key='+important_info['Gmaps_api_key'])    
#   with open('Images/test'+str(index)+'.png' , 'wb') as file:
#     print('Getting image' + str(index)+":" + str(coord))
#     file.write(r.content)
#     return tonp(r.content)

# def get_sat_pics(zoom=19):
#     global ims
#     get_zoom_in_coords()
#     count = 1
#     print("Gathering Images")
#     for idxi in range(-n+1,n):
#         i = idxi
#         print(i)
#         lat = city_center_coords[0]+i*a/69
#         for idxj in range(-n+1, n):
#           j = idxj
#           longt = city_center_coords[1] + j*b/54.6
          
#           ims[2*n-2 - (idxi+n-1)][idxj+n-1] = getimg([lat,longt],zoom, count)
#           count = count+1

# def create_Heat_Map():
#     HM = [[None for i in range(5)] for j in range(5)]
#     count = 1
#     print("Running Images through Model")
#     for i in range(5):
#         for j in range(5):
#             IMG = ims[i,j+1,:,:,:3]
#             print(count)
#             PRED = model.predict(IMG, verbose = 0)
#             INDUSTRIAL = PRED[0,0]
#             RICH = PRED[0,1]
#             SLUMS = PRED[0,2]
#             RED = SLUMS
#             GREEN = RICH
#             BLUE = INDUSTRIAL

#             RGB = [RED, GREEN, BLUE]
#             HM[i][j] = RGB
#             count = count+1

#     HM = np.array(HM)
#     return HM

# get_sat_pics()
# ims = np.array(ims)
# im = np.hstack([np.vstack(ims[:,i]) for i in range(2*n-1)])
# model = complete_Model()
# heat_Map = create_Heat_Map()

# plt.imshow(im)
# plt.show()
# plt.imshow(heat_Map)
# plt.show()

# fig, ax = plt.subplots()

# ax.imshow(im)
# ax.imshow(heat_Map, alpha = 0.5)
# plt.show()

#get_sat_pics(19)
