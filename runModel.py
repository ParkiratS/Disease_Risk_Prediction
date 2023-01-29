import wbgapi as wb
import pandas
import numpy as np
from opencage.geocoder import OpenCageGeocode
import requests
import math
import random


important_info = {'Geocode_api_key':'ccd8c35096e64bff9360bd9ef7a82032'}
city_name = input('Please type in the city you would like to see: ')



def get_GEO_Code(location):
    geocoder = OpenCageGeocode(important_info['Geocode_api_key'])
    results = geocoder.geocode(location)
    return results[0]['components']['ISO_3166-1_alpha-3']

data_collected = []
country_code = get_GEO_Code(city_name)

def find_data(data_code):
    count = 2021
    while count >= 2010:
        temp = wb.data.DataFrame(data_code, [country_code], time = [count], labels = True)[data_code][0]
        if ((temp != 0) and not (temp >= 0)):
            count = count - 1
        else:
            return temp

    return 0

data_collected.append(find_data("NY.ADJ.NNTY.PC.CD")) #Net national income per capita
data_collected.append(find_data("NY.GDP.PCAP.CD")) #GDP per capita
data_collected.append(find_data("SH.STA.WASH.P5")) #Motrality from Unsafe water
data_collected.append(find_data("SH.DTH.COMM.ZS")) #Death by communicable diseases
data_collected.append(find_data("SH.H2O.SMDW.ZS")) #Percent with safe drinking water
data_collected.append(find_data("SH.MED.BEDS.ZS")) #Hospital beds
data_collected.append(find_data("SH.MED.PHYS.ZS")) #Physicians
data_collected.append(find_data("SH.PRV.SMOK")) #Percent who smoke
data_collected.append(find_data("SH.STA.ODFC.UR.ZS")) #Open defecation
data_collected.append(find_data("SH.SGR.CRSK.ZS")) #Catastrophic expenditure for surgery
data_collected.append(find_data("SH.STA.BASS.ZS")) #Basic sanitation
data_collected.append(find_data("SI.POV.UMIC")) #Poverty headcount
data_collected.append(find_data("SN.ITK.DEFC.ZS")) #unourishment
data_collected.append(find_data("SN.ITK.SVFI.ZS")) #Food Insecurity
data_collected.append(find_data("VC.IHR.PSRC.P5")) #Homocides



data = wb.series.info()
print(data_collected)