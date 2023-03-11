# General Overview

 Welcome to the SatNet disease risk prediction software. This program works to provide a relatively inexpensive method of determining locations within cities that at the highest risk of disease outbreaks. In order to accomplish this, I utilized publically available satellite images uisng the google maps API as well as a novel hybrid residual CNN model, which is comprised of a ResNet-50, MobilNetV2, and VGG-16, in order to predict locations within cities that are most suceptible to disease outbreaks. The model is able to classify different regions as slums (poor), industrial, or low-density high-income residential which allows specific regions  to be identified as danger zones. Furthermore, the SatNet software uses  data from the World Bank API and the classification of city regions in order to generate a general disease risk index which highlights the overall danger the city faces from a disease outbreak when compared to cities across the world. My overall goal with this project was to create an inexpensive tool that people and governments across the world can use in order to identify disease hotspots where resources can be allocated to mitigate the spread of communicable diseases. The recent devestation caused by Covid-19 has shown the importance of early detection softwares as the impact the pandemic rocked the world. However, poorer countries struggle achieve early detection due to immense resources that are required for branches like the CDC and WHO. My hope is that SatNet can provide a cheap alternative for struggling countries so they can protect their citizens as effectively as everyone else!

# Description of Technology

The technical components of SatNet can be seperated into 3 main groups: satellite image collection, classification model, and the data visualization. The first step of the process is the collection of satellite images which is done through the google maps API. When the user types in the city they want to view, the GeoCode python library is used to find its coordinates and then a total of 400 evenly spaced, 640x640 resolution images are collected in a 5 mile radius around this point. In order to make these API calls, the google maps API instructions are followed as shown on the google maps website: 

https://mapsplatform.google.com/?utm_source=search&utm_medium=googleads&utm_campaign=brand_core_exa_desk_mobile_us&gclid=Cj0KCQiA6rCgBhDVARIsAK1kGPLYhJfMqzYEhzJ1zs6qi9JWR9wwJxIXu_HHiiIG9idqdjqy-3nov-4aAlL-EALw_wcB&gclsrc=aw.ds

These satellite images are then inputted into the classification algorithm which is a hybrid model consisting of a ResNet-50, MobilNetV2, and VGG-16 that has been modified to include more residual components. This final layer of the model contains a sigmoid activation function which indicates the probability of each image being a slum, industrial sector, or up-scale community. Finaly, using these outputs, a heat map is generated, where red squares indicate poverty, blue indicates industry, and green indicates wealth, which the user can use to determine disease hotspots within the city.


# Set-up Instructions

1. Download the training models folder, gatherData.py, stuff.py, and visual.py. Store all of these files and folders within one main folder.
2. Open up all of the python files and download all of the neccassary python libraries used in the software. 
3. Go to the google maps api website and create an api key. Then, copy and paste this key into the test.py file inside the top dictionary.
4. Run the software and input the city of your choice into the terminal once prompted. 
5. Wait for 7-10 minutes for the program to run and generate an output.

* The code is still in development phase and so the instructions are quite rudimentary. If you have any questions or want a more detailed set of instructions, please email me at parkiratsandhu1@gmail.com
