from math import radians, cos, sin, asin, sqrt
import numpy as np
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from . models import fare_prediction
from . serializers import fare_predictionSerializers
import pickle
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
from . forms import PredictionForm 
import os
from django.contrib import messages
from django.shortcuts import redirect
from . import forms


class Fare_predictionView(viewsets.ModelViewSet):
    queryset = fare_prediction.objects.all()
    serializer_class = fare_predictionSerializers


fare_list = []		

def ml_model(unit):
    modulePath = os.path.dirname(__file__)  # get current directory
    filePath = os.path.join(modulePath, 'fare_prediction2.pkl')
    with open(filePath, 'rb') as f:
        mdl = joblib.load(f)
        fare = mdl.predict(unit)
        print(fare)
        print(unit)
    return (round(fare[0],2))  


#@api_view(["POST"])


def pred_form(request):

    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            #name = form.cleaned_data['name']
            Pickup_Address = form.cleaned_data['Pickup_Address']
            Dropoff_Address = form.cleaned_data['Dropoff_Address']
            passenger_count = form.cleaned_data['Passengers']
            #distance = form.cleaned_data['distance']
            year = form.cleaned_data['Year']
            #JKF_distance = form.cleaned_data['JKF_distance']

            pickup_list = Pickup_Address.split(",")
            pickup_longitude = float(pickup_list[0])
            pickup_latitude = float(pickup_list[1])

            dropoff_list = Dropoff_Address.split(",")
            dropoff_longitude = float(dropoff_list[0])
            dropoff_latitude = float(dropoff_list[1])
            
            hv_distance = haversine_np(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)
            manhattan_distance = minkowski_distance(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, 1)
            euclidean_distance = minkowski_distance(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, 2)

            distance_JKF = JKF_dist(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)

            # Absolute difference in latitude and longitude
            abs_lat_diff = round(abs(dropoff_latitude - pickup_latitude), 3)
            abs_lon_diff = round(abs(dropoff_longitude - pickup_longitude), 3)

            myDict = {
                "pickup_longitude" : pickup_longitude,
                "pickup_latitude" : pickup_latitude,
                "dropoff_longitude" : dropoff_longitude,
                "dropoff_latitude" : dropoff_latitude,
                "passenger_count" : passenger_count,
                "abs_lat_diff" : abs_lat_diff,
                "abs_lon_diff" : abs_lon_diff,
                "year" : year,
                "manhattan_distance" : manhattan_distance,
                "euclidean_distance" : euclidean_distance,
                "hv_distance" : hv_distance,
                "distance_JKF" : distance_JKF,
            }
            #df = pd.DataFrame(myDict, index=[0])
            #val = np.array(df)
            val2 = [[pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count, abs_lat_diff, abs_lon_diff, year, manhattan_distance, euclidean_distance, hv_distance, distance_JKF]]
            fare = ml_model(val2)
            
            messages.success(request, 'Your Fare : ${}'.format(fare))
    form = PredictionForm()
    return render(request, 'myform/cxform.html', {'form' : form})


  


def JKF_dist(lon1, lat1, lon2, lat2):
    JFK_coord = (40.6413, -73.7781)
    pickup_JFK = haversine_np(lat1, lon1, JFK_coord[0], JFK_coord[1]) 
    dropoff_JFK = haversine_np(JFK_coord[0], JFK_coord[1], lat2, lon2)
    distance_JKF = min(pickup_JFK, dropoff_JFK)
    return (round(distance_JKF, 3))


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    hv_distance = 6371 * c  # 6371 is Radius of earth in kilometers. Use 3956 for miles
    return (round(hv_distance, 3))

def minkowski_distance(x1, x2, y1, y2, p):
    v = ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) ** (1 / p)
    return(round(v, 3))
  


def home(request):
    return render(request, 'home.html', {'name' : 'Naman'})

def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    res = val1 + val2
    return render(request, 'results.html', {'result' : res})