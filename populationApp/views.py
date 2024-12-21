from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PopulationData
from django.db import models
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth


def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    population_data = PopulationData.objects.all()
    total_population = PopulationData.objects.aggregate(models.Sum('population'))
    context = {
        'population_data': population_data,
        'total_population': total_population['population__sum'],
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')  # Use request.FILES to get the uploaded file
        if not file:
            return JsonResponse({"success": False, "message": "No file uploaded."})
        
        try:
            # Decode file for reading
            decoded_file = file.read().decode('utf-8')
            reader = csv.DictReader(decoded_file.splitlines())
            
            # Process each row
            for row in reader:
                PopulationData.objects.create(
                    lga_name=row['Name of Area'],
                    population=int(row['Population']),
                    male_population=int(row['Male Population']),
                    female_population=int(row['Female Population']),
                    year=int(row['Year']),
                    growth_rate=float(row['Growth Rate'].strip('%')),
                    density=float(row['Density (per sq. km)']),
                    households=int(row['Households'])
                )
            
            return JsonResponse({"success": True, "message": "Data uploaded successfully."})
        
        except KeyError as e:
            return JsonResponse({"success": False, "message": f"Missing column in CSV: {str(e)}"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error uploading data: {str(e)}"})
    
    return render(request, "upload.html")


def get_population_data(request):
    # Fetch data for the charts
    population_data = PopulationData.objects.all()
    lgas = []
    populations = []
    male_population = 0
    female_population = 0

    for data in population_data:
        lgas.append(data.lga_name)
        populations.append(data.population)
        male_population += data.male_population
        female_population += data.female_population

    # Prepare data for JSON response
    data = {
        "lgas": lgas,
        "populations": populations,
        "gender_distribution": {
            "Male": male_population,
            "Female": female_population
        }
    }
    return JsonResponse(data)

@login_required(login_url='login')
def clear_data(request):
    if request.method == 'POST':
        try:
            # Delete all entries in the PopulationData table
            PopulationData.objects.all().delete()
            return JsonResponse({"success": True, "message": "All data cleared successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error clearing data: {str(e)}"})
    return render(request, "clear_data.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return JsonResponse({"success": True, "message": "Login Successfully..."})
        else:
            return JsonResponse({"success": False, "message": "Login Failed!! Invalid Credentials !"})
    return render(request, "login.html")
