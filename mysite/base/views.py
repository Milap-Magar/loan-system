from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


from .forms import CreateUserForm
from django.contrib import messages

# 
import numpy as np
import pandas as pd
import joblib
from joblib import load

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import os



# Create your views here.


def signupPage(request):
    form = CreateUserForm()
    if request.method=='POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            messages.success(request, 'Account  created for '+ user)
            return redirect('landing')
    
    context = { 'form': form } 
    return render(request, 'signup.html', context) 

def LandingPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    return render (request,'landing.html')
    


        

@login_required(login_url='landing')
def Home(request):
    return render (request,'home.html')




def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='landing')
def DataAnalysis(request):
    return  render (request,'dataanalysis.html')

@login_required(login_url='landing')
def Predict(request):
    return  render(request,'predict.html')




def getPredictions(martial, house_O, car_O, profession, city, state, current_jy, current_hy, income, age):
    model = load(filename = './savedModels/model.pkl')
    encoders = load(filename = './savedModels/encoders.sav')

    categorical_data = [martial, house_O, car_O, profession, city, state]
    for i, j in enumerate(categorical_data):
        categorical_data[i] = [j]
    categorical_columns = ['Married/Single', 'House_Ownership', 'Car_Ownership', 'Profession', 'CITY', 'STATE']

    for i, column in enumerate(categorical_columns):
        label_encoder = encoders[column]
        categorical_data[i] = label_encoder.transform(categorical_data[i])
     
    categorical_data = np.squeeze(categorical_data)

    if income <= 375000:
        income = 0
    elif 375000 < income <= 750000:
        income = 1
    elif 750000 < income <=2250000:
        income = 2
    else:
        income = 3

    if age <= 32:
        age = 0
    elif 32 < age <= 44:
        age = 1
    elif 44 < age <= 56:
        age = 2
    elif 56 < age <= 68:
        age = 3
    else:
        age = 4  
        
    data = [[categorical_data[0], categorical_data[1], categorical_data[2], categorical_data[3], categorical_data[4], categorical_data[5], current_jy, current_hy, income, age]]
    df = pd.DataFrame(data , columns = model.feature_names_in_)
        
    prediction = model.predict(df)
    
    if prediction == 0:
        return 'eligible'
    elif prediction == 1:
        return 'not eligible'
    else:
        return 'error'
    
@login_required(login_url='landing')
def Result(request):
    marital = request.GET['martial']
    house_O = request.GET['house_O']
    car_O = request.GET['car_O']
    profession = request.GET['profession']
    city= request.GET['city']
    state = request.GET['state']
    current_jy = int(request.GET['current_jy'])
    current_hy = int(request.GET['current_hy'])
    income = int(request.GET['income'])
    age = int(request.GET['age'])

    result = getPredictions(marital, house_O, car_O, profession, city, state, current_jy, current_hy, income, age)


    return render(request, 'result.html',{'result' : result})
