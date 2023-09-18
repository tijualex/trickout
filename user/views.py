import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout,login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from django.shortcuts import get_object_or_404


from customadmin import models, views
from .models import UserProfile, User
from django.contrib.auth.decorators import login_required
from .models import PersonMeasurement 
from customadmin.models import BottomPattern, Designs, DressType, NeckPattern, SleevesPattern
from customadmin.models import Fabric, TopPattern  # Import your Fabric model



from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages

# Replace 'User' with your custom user model
User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            # User is authenticated, perform login
            login(request, user)
            
            # Redirect to the appropriate page
            if user.is_superuser:
                request.session['username'] = user.username
                return redirect('admin_index')
            else:
                request.session['username'] = user.username
                return redirect('index')
        else:
            messages.info(request, "Invalid Login")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



    

    
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('signup')
            else:
                obj = User(name=name, username=username, email=email)
                obj.set_password(password)
                obj.save()
                return redirect('login_view')
        else:
            messages.info(request, "Passwords do not match")
            return redirect('signup')
    return render(request, 'signup.html')









from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

def index(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # If the user is authenticated, check if they are an admin
        if request.user.is_superuser:
            # If the user is an admin, redirect to the admin dashboard or any other desired page
            return redirect('admin_index')  # Replace 'admin_dashboard' with the appropriate URL name
        else:
            # For authenticated non-admin users, display the regular index page
            return render(request, 'index.html')
    else:
        # For unauthenticated users, display the regular index page
        return render(request, 'index.html')


# @login_required()
# def index(request):
#     return render(request,'index.html')

def logout_view(request):
    print('Logged Out')
    logout(request)
    if 'username' in request.session:
        del request.session['username']
        request.session.clear()
    return redirect('index')


#username checking
def check_username_exists(request):
    username = request.GET.get('username')
    data = {'exists': User.objects.filter(username=username).exists()}
    return JsonResponse(data)


@login_required(login_url='login_view')
def measurement_view(request, design_id):
    try:
        # Fetch the design based on the provided design_id
        design = Designs.objects.get(pk=design_id)
        
        if request.method == 'POST':
            # Retrieve the submitted form data
            waist = request.POST['waist']
            waist_unit = request.POST['waistUnit']
            shoulder = request.POST['shoulder']
            shoulder_unit = request.POST['shoulderUnit']
            chest = request.POST['chest']
            chest_unit = request.POST['chestUnit']
            hip = request.POST['hip']
            hip_unit = request.POST['hipUnit']
            inseam = request.POST['Inseam']
            inseam_unit = request.POST['inseamUnit']

            # Convert measurements to a consistent unit (e.g., inches or centimeters)
            # Define conversion factors as needed
            inches_to_cm = 2.54

            if waist_unit == 'cm':
                waist = float(waist) / inches_to_cm
            if shoulder_unit == 'cm':
                shoulder = float(shoulder) / inches_to_cm
            if chest_unit == 'cm':
                chest = float(chest) / inches_to_cm
            if hip_unit == 'cm':
                hip = float(hip) / inches_to_cm
            if inseam_unit == 'cm':
                inseam = float(inseam) / inches_to_cm

            # Create a new measurement associated with the currently authenticated user and the design
            measurement = PersonMeasurement(
                user=request.user,  # Assign the currently authenticated user
                waist=waist,
                shoulder=shoulder,
                chest=chest,
                hips=hip,
                inseam_length=inseam,
                design=design  # Associate the measurement with the design
            )
            measurement.save()

            # Redirect to a success page or another appropriate action
            return redirect('index')

        return render(request, 'design/measurement.html')

    except Designs.DoesNotExist:
        return HttpResponse("Design not found")


@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create one for the user
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            user_profile.profile_pic = profile_pic

        user_profile.name = name
        user_profile.phone_number = phone_number
        user_profile.address = address
        request.user.email = email

        user_profile.save()
        request.user.save()
        # messages.success(request, "Profile updated successfully")
        return redirect('profile')
    
    return render(request, 'userprofile/user_profile.html', {'user_profile': user_profile})






# design views
def design(request):
    dress_types = DressType.objects.all()  # Retrieve all dress types

    context = {
        'dress_types': dress_types,
    }

    return render(request, 'design/design.html', context)




def dress_detail(request, dress_type):
    dress_type = get_object_or_404(DressType, dress_type=dress_type)
    
    # Retrieve options for each pattern type based on the selected dress type
    fabric = Fabric.objects.all()
    bottom_patterns = BottomPattern.objects.filter(dress_type=dress_type)
    neck_patterns = NeckPattern.objects.filter(dress_type=dress_type)
    top_patterns = TopPattern.objects.filter(dress_type=dress_type)
    sleeves_patterns = SleevesPattern.objects.filter(dress_type=dress_type)

    context = {
        'dress_type': dress_type,
        'neck_patterns': neck_patterns,
        'bottom_patterns': bottom_patterns,
        'top_patterns': top_patterns,
        'sleeves_patterns': sleeves_patterns,
        'fabric': fabric,
    }

    return render(request, 'design/dress_detail.html', context)

def pattern_details(request, pattern_id):
    # Get the pattern option based on pattern_id
    pattern_option = get_object_or_404(PatternOption, pk=pattern_id)

    context = {
        'pattern_option': pattern_option,
    }

    return render(request, 'design/pattern_details.html', context)


# confirm design


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import ast

def confirm_design(request):
    if request.method == 'POST':
        # Retrieve the pattern IDs from the POST request
        selected_fabric_pattern_str = request.POST.get('selectedFabricPattern')
        selected_neck_pattern_str = request.POST.get('selectedNeckPattern')
        selected_top_pattern_str = request.POST.get('selectedTopPattern')
        selected_sleeves_pattern_str = request.POST.get('selectedSleevesPattern')
        selected_bottom_pattern_str = request.POST.get('selectedBottomPattern')

        # Initialize lists to store selected pattern names and IDs
        selected_pattern_id = []
        selected_patterns = []

        # Fetch the pattern names from the database and handle errors gracefully
        def get_pattern_name(pattern_str, pattern_model):
            try:
                pattern_id = int(pattern_str)
                selected_pattern = get_object_or_404(pattern_model, pk=pattern_id)
                selected_pattern_id.append(selected_pattern.custom_id)
                selected_patterns.append(selected_pattern.name)
            except (ValueError, pattern_model.DoesNotExist):
                selected_patterns.append('Pattern Not Found')

        get_pattern_name(selected_fabric_pattern_str, Fabric)
        get_pattern_name(selected_neck_pattern_str, NeckPattern)
        get_pattern_name(selected_top_pattern_str, TopPattern)
        get_pattern_name(selected_sleeves_pattern_str, SleevesPattern)
        get_pattern_name(selected_bottom_pattern_str, BottomPattern)

        try:
            top_pattern_id = int(selected_top_pattern_str)
            selected_top_pattern = get_object_or_404(TopPattern, pk=top_pattern_id)

            # Retrieve the associated DressType
            selected_dress_type = selected_top_pattern.dress_type

            # Append DressType to the selected_patterns list
            selected_patterns.append(selected_dress_type.dress_type)
            selected_pattern_id.append(selected_dress_type.dress_type)

        except (ValueError, TopPattern.DoesNotExist):
            selected_patterns.append('TopPattern Not Found')

        # Calculate the total price (you should have this logic implemented)
        total_price = 100  # Replace with your actual calculation logic

        # Render the template with the selected pattern names and total price
        return redirect('display_selected_patterns', selected_patterns=selected_patterns, selected_pattern_id=selected_pattern_id, total_price=total_price)
    else:
        # Handle the case when the request method is not POST (e.g., redirect or show an error)
        return HttpResponse("Invalid Request")


def display_selected_patterns(request, selected_patterns, selected_pattern_id, total_price):
    # Replace these with your actual data
    selected_patterns_list = ast.literal_eval(selected_patterns)
    selected_patterns_id_list = ast.literal_eval(selected_pattern_id)

    # Create dictionaries for selected patterns and pattern IDs
    selected_patterns_dict = {
        'fabric': selected_patterns_list[0],
        'neck': selected_patterns_list[1],
        'top': selected_patterns_list[2],
        'sleeves': selected_patterns_list[3],
        'bottom': selected_patterns_list[4],
        'desstype': selected_patterns_list[5],
    }

    selected_pattern_id_dict = {
        'fabric_id': selected_patterns_id_list[0],
        'neck_id': selected_patterns_id_list[1],
        'top_id': selected_patterns_id_list[2],
        'sleeves_id': selected_patterns_id_list[3],
        'bottom_id': selected_patterns_id_list[4],
        'desstype_id': selected_patterns_id_list[5],
    }

    total_price = 100  # Replace with your actual calculation logic

    context = {
        'selected_patterns': selected_patterns_dict,
        'selected_patterns_id': selected_pattern_id_dict,
        'total_price': total_price,
    }

    return render(request, 'design/confirm_design.html', context)

import json

def create_design(request):
    if request.method == 'POST':
        # Retrieve the selected patterns and dress type from the form data
        fabric_id = request.POST.get('fabric_id')
        neck_id = request.POST.get('neck_id')
        top_id = request.POST.get('top_id')
        sleeves_id = request.POST.get('sleeves_id')
        bottom_id = request.POST.get('bottom_id')
        desstype = request.POST.get('desstype_id')

        # Get instances of the pattern models using the IDs
        try:
            fabric_pattern = get_object_or_404(Fabric, pk=fabric_id)
            neck_pattern = get_object_or_404(NeckPattern, pk=neck_id)
            top_pattern = get_object_or_404(TopPattern, pk=top_id)
            sleeves_pattern = get_object_or_404(SleevesPattern, pk=sleeves_id)
            bottom_pattern = get_object_or_404(BottomPattern, pk=bottom_id)
            desstype = get_object_or_404(DressType, pk=desstype)

            # Assuming you have the necessary data to create a Designs object
            user = request.user  # Get the current user

            try:
                # Create the Designs object with the retrieved instances
                design = Designs.objects.create(
                    user=user,
                    dress_type=desstype,
                    neck_pattern=neck_pattern,
                    sleeves_pattern=sleeves_pattern,
                    bottom_pattern=bottom_pattern,
                    top_pattern=top_pattern,
                    fabric1=fabric_pattern,
                )

                # Redirect to the third view ('measurement_view') with design_id as a parameter
                return redirect('measurement_view', design_id=design.design_id)
            except Exception as e:
                # Handle exceptions appropriately (e.g., show an error message)
                return HttpResponse(f"Error: {e}")

        except NeckPattern.DoesNotExist:
            return HttpResponse("NeckPattern not found")  # Handle the case when NeckPattern doesn't exist

    else:
        # Handle the case when the request method is not POST (e.g., redirect or show an error)
        return HttpResponse("Invalid Request")