import csv
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Democsv


@login_required(login_url='login')
@csrf_exempt  # Only use this if you're skipping CSRF for this specific endpoint (not recommended for production)
def home_view(request):
    is_superuser = request.user.is_superuser
    if request.method == 'POST' and request.FILES.get('csv_file') and is_superuser:
        csv_file = request.FILES['csv_file']
        
        # Check if the file is a CSV
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'errors': 'Please upload a valid CSV file.'})

        try:
            # Open the file and read CSV data
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            next(csv_reader)  # Skip the header row if your CSV has headers

            # Import data into your model (assuming you have columns in the CSV that match model fields)
            for row in csv_reader:
                # Ensure you have the correct number of columns based on your model
                model_instance = Democsv(field1=row[0], field2=row[1], field3=row[2])  # Replace with actual fields
                model_instance.save()

            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})

    # Fetch all data from the Democsv model
    demo_data = Democsv.objects.all()

    # Render the home page with the demo data
    return render(request, 'accounts/home.html', {'demo_data': demo_data,'is_superuser': is_superuser})


@method_decorator(csrf_exempt, name='dispatch')
def ajax_register(request):
    if request.user.is_authenticated:
        return redirect('home') 
    form = CustomUserCreationForm()  # Initialize the form for GET requests
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Re-initialize the form with POST data
        if form.is_valid():
            user = form.save()
            # Return a success message with a redirect URL for the login page
            return JsonResponse({
                'success': True,
                'message': 'User registered successfully!',
                'redirect_url': '/login/'  # You can change this URL to match your login URL
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # If it's a GET request, simply return the form
    return render(request, 'accounts/ajax-register.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


