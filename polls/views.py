from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import pickle as pk
import pandas as pd
import numpy as np
import os
from polls.models import Data
from django.conf import settings
model_path = os.path.join(settings.BASE_DIR, 'mysite', 'static', 'model', 'model.pkl')
scaler_path = os.path.join(settings.BASE_DIR, 'mysite', 'static', 'model', 'scaler.pkl')

with open(model_path, 'rb') as model_file:
    model = pk.load(model_file)

with open(scaler_path, 'rb') as scaler_file:
    scaler = pk.load(scaler_file)

def home(request):
    return render(request, "index1.html")

def get(request):
    if request.method == 'GET':
        phone_regex = RegexValidator(
       
        regex=r'^[6-9]\d{9}$',
        )
        name = request.GET.get("name")
        contact=request.GET.get("Contact")
        std=request.GET.get("std")
        data=''
        try: 
            phone_regex(contact)
        except:
            data="please enter valid phone number"
            return render(request,"index1.html",{"data":data})

        Data.objects.create(name=name,contact=contact,std=std)
        HoursStudied = request.GET.get("HoursStudied")
        PreviousScores = request.GET.get("PreviousScores")
        Sleep = request.GET.get("Sleep")
        Sample = request.GET.get("Sample")
        print("Sample:", Sample)
        if HoursStudied and PreviousScores and Sleep and Sample: 
                pred_data = pd.DataFrame([[HoursStudied, PreviousScores, Sleep, Sample]],
                                         columns=['HoursStudied', 'PreviousScores', 'Sleep Hours', 'Sample Question Papers Practiced'])
                pred_data_scaled = scaler.transform(pred_data)
                predict = model.predict(pred_data_scaled)
                predicted_value = int(predict[0])
                print("Predicted Value:", predicted_value)
                return render(request, "index1.html", {'prediction': predicted_value,"std":std,"data":data})
            
        else:
            return render(request, "index1.html", {'error': 'Please fill all the fields.'})

    return render("/")

def Show(request):
    data = Data.objects.all()
    return render(request, "show.html", {"data": data})