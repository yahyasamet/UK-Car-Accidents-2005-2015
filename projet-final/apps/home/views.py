# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from joblib import load

model= load('C:/Users/samet/Desktop/projet-final/apps/savedModeles/model.joblib')

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

            


@login_required(login_url="/login/") 
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    


    try:

        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        
        if load_template =='predictions.html':
            if request.method =='POST':
                number_of_vehicules = request.POST['number_of_vehicules']
                light_condition = request.POST['light_condition']
                weather_condition = request.POST['weather_condition']
                Road_Surface_Condition = request.POST['Road_Surface_Condition']
                Special_Conditions_at_Site = request.POST['Special_Conditions_at_Site']
                y_pred=model.predict([[light_condition,weather_condition,Road_Surface_Condition,Special_Conditions_at_Site,number_of_vehicules]])
                print(y_pred[0])
                if y_pred[0] == '1':
                    y_pred='low'
                elif y_pred[0] == '2':
                    y_pred='medium'
                elif y_pred[0] == '3':
                    y_pred='high'
                print(y_pred)
                return render(request,'home/predictions.html',{'result' : y_pred})
            return render(request,'home/predictions.html')




        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

