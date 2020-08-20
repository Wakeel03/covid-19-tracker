from django.shortcuts import render
import http.client
import requests, json
from .forms import CountryForm
from django.http import HttpResponseRedirect

def index(request):

    days = "20"

    url_all_countries = "https://disease.sh/v3/covid-19/countries?yesterday=true"
    url_historic_data_all = "https://disease.sh/v3/covid-19/historical/all?lastdays="+days
    url_specific_country = "https://disease.sh/v3/covid-19/countries/"
    url_all = "https://disease.sh/v3/covid-19/all"
    url_historic_data_specific_country = "https://disease.sh/v3/covid-19/historical/"
    current_id = 1
    
    country = "Worldwide"
    selected_id = 1
    countries = [{
        'id' : 1,
        'name' : 'Worldwide'
    }]

    data_all_countries = requests.get(url_all_countries).json()
    
    for c in data_all_countries:
        current_id += 1
        countries.append({
            'id' : current_id,
            'name' : c['country'],
        })


    if request.method == 'POST':
        country_id = request.POST['country']
        country = countries[int(country_id)-1]['name']
        selected_id = int(country_id)
        days = request.POST['days']
        url_historic_data_all = "https://disease.sh/v3/covid-19/historical/all?lastdays="+days

    if country == "Worldwide":
        url = url_all
        history_url = url_historic_data_all
        history_data = requests.get(history_url).json()

    else:
        url = url_specific_country + country + "?yesterday=true"
        history_url = url_historic_data_specific_country + country+ "?lastdays=" + days
        history_data = requests.get(history_url).json()['timeline']
    
    data = requests.get(url).json()
    dates = []
    history_cases = []
    history_deaths = []
    history_recovered = []

    for d in history_data['cases']:
        dates.append(d)
        history_cases.append(history_data['cases'][d])
        history_deaths.append(history_data['deaths'][d])
        history_recovered.append(history_data['recovered'][d])

    context = {
        'days' : days,
        'data' : data,
        'countries' : countries,
        'current_country_selected' : selected_id,
        'dates' : dates,
        'history_cases' : history_cases,
        'history_deaths' : history_deaths,
        'history_recovered' : history_recovered
    }
    return render(request, 'tracker/index.html', context)

