from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .form import LocationForm
from .models import WeatherEvent
import requests
import logging
from datetime import datetime
import io
import base64
import matplotlib.pyplot as plt
import folium


# Create your views here.
from django.shortcuts import render
# Configuration (make sure to set these in your Django settings or environment variables)
API_KEY = '012c37a81427166fc7b5ef9e6e183457'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'
FLOOD_RISK_THRESHOLD = 50
DROUGHT_RISK_THRESHOLD = 5

LOCATIONS = [
    "Nairobi, Kenya", "Lagos, Nigeria", "Cairo, Egypt", "Johannesburg, South Africa",
    "Addis Ababa, Ethiopia", "Accra, Ghana", "Dakar, Senegal", "Casablanca, Morocco",
    "Kampala, Uganda", "Dar es Salaam, Tanzania"
]

def home(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            return redirect('monitor_location', location=location)
    else:
        form = LocationForm()
    
    return render(request, 'home.html', {'form': form})



def map_dashboard(request):
    return render(request,'map_dashboard.html')

def reports(request):
    return render(request, 'reports.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def alerts(request):
    return render(request,'alerts.html')


from google.cloud import texttospeech



import requests
from django.http import JsonResponse

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            body = json.loads(request.body)
            message = body.get('message')
            
            # Your API key and endpoint
            YOUR_API_KEY = "AIzaSyAH81fCgUSgbY6WdDnojPNGPmyHzjzQ_hw"
            url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={YOUR_API_KEY}'
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": message}
                        ]
                    }
                ]
            }
            
            # Make the API request
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_json = response.json()
            bot_response = response_json['candidates'][0]['content']['parts'][0]['text']
            
            
            # Return the response as JSON
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_weather_forecast(location):
    # Fetch weather data
    endpoint = f'{BASE_URL}forecast'
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for {location}: {e}")
        return None

def analyze_weather_risk(forecast_data):
    # Analyze weather risk
    flood_risk_periods = []
    total_precipitation = 0
    for forecast in forecast_data.get('list', []):
        date = datetime.fromtimestamp(forecast['dt'])
        precipitation = forecast.get('rain', {}).get('3h', 0)
        total_precipitation += precipitation
        if precipitation > FLOOD_RISK_THRESHOLD:
            risk_level = "High" if precipitation > FLOOD_RISK_THRESHOLD * 1.5 else "Moderate"
            flood_risk_periods.append((date, precipitation, "Flood", risk_level))
    if total_precipitation < DROUGHT_RISK_THRESHOLD:
        drought_risk_level = "High" if total_precipitation < DROUGHT_RISK_THRESHOLD / 2 else "Moderate"
        flood_risk_periods.append((date, total_precipitation, "Drought", drought_risk_level))
    return flood_risk_periods

def monitor_location(request, location):
    # Monitor weather for a location
    forecast_data = get_weather_forecast(location)
    if not forecast_data:
        return JsonResponse({"error": "Unable to fetch weather forecast data."}, status=500)

    risk_periods = analyze_weather_risk(forecast_data)
    map_html = visualize_weather_risk(location, risk_periods)
    graph_data = create_precipitation_graph(location, forecast_data)
    historical_data = analyze_historical_data(location)

    return render(request, 'monitor_location.html', {
        'location': location,
        'map_html': map_html,
        'graph_data': graph_data,
        'historical_data': historical_data,
    })

def visualize_weather_risk(location, risk_periods):
    # Visualize weather risk on a map using Folium
    # Use static coordinates or fetch them dynamically
    coordinates = {
        "Nairobi, Kenya": {'lat': -1.2921, 'lon': 36.8219},
        "Lagos, Nigeria": {'lat': 6.5244, 'lon': 3.3792},
        "Cairo, Egypt": {'lat': 30.0444, 'lon': 31.2357},
        "Johannesburg, South Africa": {'lat': -26.2041, 'lon': 28.0473},
        "Addis Ababa, Ethiopia": {'lat': 9.145, 'lon': 40.489673},
        "Accra, Ghana": {'lat': 5.6037, 'lon': -0.1870},
        "Dakar, Senegal": {'lat': 14.6928, 'lon': -17.4467},
        "Casablanca, Morocco": {'lat': 33.5731, 'lon': -7.5890},
        "Kampala, Uganda": {'lat': 0.3476, 'lon': 32.5825},
        "Dar es Salaam, Tanzania": {'lat': -6.7924, 'lon': 39.2083}
    }.get(location, {'lat': 0, 'lon': 0})  # Default coordinates if location is unknown
    
    m = folium.Map(location=[coordinates['lat'], coordinates['lon']], zoom_start=10)
    for date, precipitation, event_type, risk_level in risk_periods:
        color = 'red' if risk_level == "High" else 'orange'
        folium.Marker(
            location=[coordinates['lat'], coordinates['lon']],
            popup=f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}<br>Event: {event_type}<br>Precipitation: {precipitation} mm<br>Risk Level: {risk_level}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    return m._repr_html_()

def create_precipitation_graph(location, forecast_data):
    # Create a precipitation graph using Matplotlib
    dates = []
    precipitations = []
    for forecast in forecast_data.get('list', [])[:8]:
        date = datetime.fromtimestamp(forecast['dt'])
        precipitation = forecast.get('rain', {}).get('3h', 0)
        dates.append(date)
        precipitations.append(precipitation)
    
    plt.figure(figsize=(10, 5))
    plt.bar(dates, precipitations)
    plt.title(f'Precipitation Forecast for {location} (Next 24 Hours)')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return graph_data

def analyze_historical_data(location):
    # Analyze historical data (placeholder for now)
    return "No historical data available for analysis."