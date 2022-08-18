from opencage.geocoder import OpenCageGeocode
import requests

location = input('Please type in the city you would like to see: ')

key = 'ccd8c35096e64bff9360bd9ef7a82032'
geocoder = OpenCageGeocode(key)
query = location
results = geocoder.geocode(query)
center = (results[0]['geometry']['lat'] , results[0]['geometry']['lng'])






api_key = "AIzaSyBwVPcm0csBOu_qgM0P4ruhXihSNojUF8I"
  

url = "https://maps.googleapis.com/maps/api/staticmap?"
  
# get method of requests module
# return response object
r = requests.get('https://maps.googleapis.com/maps/api/staticmap?center=' +str(center[0]) + ',' + str(center[1]) + '&zoom=19&size=1000x1000&maptype=satellite&format=png8&key=AIzaSyBwVPcm0csBOu_qgM0P4ruhXihSNojUF8I')
  
# wb mode is stand for write binary mode

with open('test.png', 'wb') as file:
   # writing data into the file
   file.write(r.content)