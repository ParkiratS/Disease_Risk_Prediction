import wbgapi as wb
import pandas
import numpy as np
from opencage.geocoder import OpenCageGeocode
import requests
import math
import random



def find_data(data_code, country_code):
    count = 2021
    while count >= 2000:
        temp = wb.data.DataFrame(data_code, [country_code], time = [count], labels = True)[data_code][0]
        if ((temp != 0) and not (temp >= 0)):
            count = count - 1
        else:
            return temp

    return 0

def WBData(country_code):
    data_collected = []
    data_collected.append(find_data("NY.ADJ.NNTY.PC.CD", country_code)) #Net national income per capita
    data_collected.append(find_data("NY.GDP.PCAP.CD", country_code)) #GDP per capita
    data_collected.append(find_data("SH.STA.WASH.P5", country_code)) #Motrality from Unsafe water (Delete)
    data_collected.append(find_data("SH.DTH.COMM.ZS", country_code)) #Death by communicable diseases
    data_collected.append(100-find_data("SH.H2O.SMDW.ZS", country_code)) #Percent with safe drinking water
    data_collected.append(find_data("SH.PRV.SMOK", country_code)) #Percent who smoke
    data_collected.append(find_data("SH.SGR.CRSK.ZS", country_code)) #Catastrophic expenditure for surgery
    data_collected.append(100-find_data("SH.STA.BASS.ZS", country_code)) #Basic sanitation
    data_collected.append(find_data("SI.POV.UMIC", country_code)) #Poverty headcount
    data_collected.append(find_data("SN.ITK.DEFC.ZS", country_code)) #unourishment
    data_collected.append(find_data("SN.ITK.SVFI.ZS", country_code)) #Food Insecurity
    data_collected.append(find_data("VC.IHR.PSRC.P5", country_code)) #Homocides
    return data_collected



data = wb.series.info()


