from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
    
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