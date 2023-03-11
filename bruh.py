import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as imread
import os
import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, ZeroPadding2D, AveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet_v2 import ResNet50V2 as ResNet
from tensorflow.keras.applications.densenet import DenseNet121 as DenseNet
from tensorflow.keras.applications.inception_v3 import InceptionV3 as inceptionNet
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2 as MobileNet

def create_Model():
    input_ = Input(shape = (640,640,3))
    
    Res = ResNet(include_top=False, weights='imagenet', input_tensor=input_, pooling='average', classifier_activation = 'softmax')
    Inception = inceptionNet(include_top = False, weights = 'imagenet', input_tensor = input_, pooling = 'average', classifier_activation = 'softmax')
    
    Inception_mid_In = Inception.get_layer('mixed1').output
    Inception_mid_pad = ZeroPadding2D(padding = ((1,2),(2,1)))(Inception_mid_In)
    
    Res_mid_In = Res.get_layer('conv3_block1_out').output
    
    mid_concatenation = tf.keras.layers.Concatenate(axis = -1)([Res_mid_In, Inception_mid_pad])
    mid_concatenation_conv2D1 = Conv2D(1024, (1,1), activation='relu', padding='same')(mid_concatenation)
    mid_concatenation_padding = ZeroPadding2D(padding = (0,0))(mid_concatenation_conv2D1)
    mid_concatenation_conv2D2 = Conv2D(3, (1,1), activation='relu', padding='same')(mid_concatenation_padding)
    
    
    MNet = MobileNet(include_top = False, weights = None, input_tensor = mid_concatenation_conv2D2, pooling = 'average', classifier_activation = 'softmax')
    MNet_Out_flatten = Flatten()(MNet.output)
    MNet_Out_Dense1 = Dense(256, activation = 'sigmoid')(MNet_Out_flatten)
    MNet_Out_Dense2 = Dense(64, activation = 'sigmoid')(MNet_Out_Dense1)

    Res_Out_flatten = Flatten()(Res.output)
    Res_Out_Dense1 = Dense(512, activation = 'sigmoid')(Res_Out_flatten)
    Res_Out_Dense2 = Dense(128, activation = 'sigmoid')(Res_Out_Dense1)
    Res_Out_Dense3 = Dense(64, activation = 'sigmoid')(Res_Out_Dense2)
    
    Inception_Out_flatten = Flatten()(Inception.output)
    Inception_Out_Dense1 = Dense(128, activation = 'sigmoid')(Inception_Out_flatten)
    Inception_Out_Dense2 = Dense(64, activation = 'sigmoid')(Inception_Out_Dense1)
    
    Res_Res_input = Res.get_layer('conv4_block3_out').output
    Res_Res_Conv1 = Conv2D(64, (2,2), activation='relu', padding='same')(Res_Res_input)
    Res_Res_Conv2 = Conv2D(8, (2,2), activation='relu', padding='same')(Res_Res_Conv1)
    Res_Res_flatten = Flatten()(Res_Res_Conv2)
    Res_Res_Dense1 = Dense(128, activation = 'sigmoid')(Res_Res_flatten)
    Res_Res_Dense2 = Dense(64, activation = 'sigmoid')(Res_Res_Dense1)
    
    Inception_Res_input = Inception.get_layer('mixed5').output
    Inception_Res_Conv1 = Conv2D(64, (2,2), activation='relu', padding='same')(Inception_Res_input)
    Inception_Res_Conv2 = Conv2D(8, (2,2), activation='relu', padding='same')(Inception_Res_Conv1)
    Inception_Res_flatten = Flatten()(Inception_Res_Conv2)
    Inception_Res_Dense1 = Dense(128, activation = 'sigmoid')(Inception_Res_flatten)
    Inception_Res_Dense2 = Dense(64, activation = 'sigmoid')(Inception_Res_Dense1)
    
    
    
    concatenation_out = tf.keras.layers.Concatenate(axis = -1)([Res_Out_Dense3, Inception_Out_Dense2, MNet_Out_Dense2, Res_Res_Dense2, Inception_Res_Dense2])
    
    FStage_Dense1 = Dense(512, activation='sigmoid', name='FStage_Dense1')(concatenation_out)
    FStage_Dense2 = Dense(64, activation='sigmoid', name='FStage_Dense2')(FStage_Dense1)
    FStage_Dense3 = Dense(8, activation='sigmoid', name='FStage_Dense3')(FStage_Dense2)
    
    output_ = Dense(3, activation='sigmoid', name='output_')(FStage_Dense3)
    model = Model(input_, output_)
    
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return model

def complete_Model():
    model1 = create_Model()
    model1.load_weights("best_model.hdf5")
    return model1

