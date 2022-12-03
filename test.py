import math

# from opencage.geocoder import OpenCageGeocode
# import requests
# import os




# location = input('Please type in the city you would like to see: ')

# key = 'ccd8c35096e64bff9360bd9ef7a82032'
# geocoder = OpenCageGeocode(key)
# query = location
# results = geocoder.geocode(query)
# #center = (results[0]['geometry']['lat'] , results[0]['geometry']['lng'])
# center = (14.582664, 121.004210)





# api_key = "AIzaSyBwVPcm0csBOu_qgM0P4ruhXihSNojUF8I"
# zoom = 18

# url = "https://maps.googleapis.com/maps/api/staticmap?"
  
# # get method of requests module
# # return response object
  
# r = requests.get('https://maps.googleapis.com/maps/api/staticmap?center=' +str(center[0]) + ',' + str(center[1]) + '&zoom=' + str(zoom) + '&size=5000x5000&maptype=satellite&format=png8&key='+api_key)
# file = open('Images/test.png', 'wb')
# file.write(r.content)

print(math.cos(14*((math.pi)/180))*69)