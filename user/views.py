from decimal import Decimal
from urllib.parse import quote, unquote
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings
from .models import PersonMeasurement, UserProfile 
from customadmin.models import BottomPattern, Designs, DressType, NeckPattern, SleevesPattern
from customadmin.models import Fabric, TopPattern  # Import your Fabric model
 

# Replace 'User' with your custom user model
User = get_user_model()

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.user.is_authenticated:
        # User is already authenticated, redirect to the desired page (e.g., 'index')
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, perform login
            login(request, user)

            # Redirect to the appropriate page after login
            if user.is_superuser:
                # If the user is an admin, redirect to an admin page
                return redirect('admin_index')
            else:
                # If the user is not an admin, redirect to a regular user page (e.g., 'index')
                return redirect('index')
        else:
            # Invalid login credentials, display an error message
            messages.error(request, "Invalid Login")
            return render(request, 'login.html')

    return render(request, 'login.html')




    

    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')

        # Check if any of the values are null
        if not (name and username and email and password and cpassword):
            messages.error(request, "Please fill in all the fields")
            return redirect('signup')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken")
                return redirect('signup')
            else:
                # Create a new user using Django's User model
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = name
                user.save()
                subject = 'Your account has been created'
                message = 'Your account has been created successfully.'
                from_email = settings.EMAIL_HOST_USER  # Your sender email address
                recipient_list = [user.email]

                send_mail(subject, message, from_email,recipient_list)
                
                return redirect('login_view')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
    return render(request, 'signup.html')










from django.shortcuts import render, redirect

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
            inseam_unit = request.POST['InseamUnit']

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

            # Redirect to the order confirmation page with the design_id
            return redirect('order_confirmation_view', design_id=design_id)

        return render(request, 'design/measurement.html', {'design_id': design_id})

    except Designs.DoesNotExist:
        return HttpResponse("Design not found")


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if profile_pic:
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
                selected_pattern_id.append('Pattern Not Found')

        get_pattern_name(selected_fabric_pattern_str, Fabric)
        get_pattern_name(selected_top_pattern_str, TopPattern)
        get_pattern_name(selected_neck_pattern_str, NeckPattern)
        get_pattern_name(selected_sleeves_pattern_str, SleevesPattern)
        get_pattern_name(selected_bottom_pattern_str, BottomPattern)

        try:
            top_pattern_id = int(selected_top_pattern_str)
            neck_pattern_id = int(selected_neck_pattern_str)
            bottom_pattern_id = int(selected_bottom_pattern_str)
            top_sleeves_id = int(selected_sleeves_pattern_str)
            top_fabric_id = int(selected_fabric_pattern_str)
            
            selected_top_pattern = get_object_or_404(TopPattern, pk=top_pattern_id)
            selected_neck_pattern =get_object_or_404(NeckPattern, pk=neck_pattern_id)
            selected_sleeves_pattern = get_object_or_404(SleevesPattern, pk=top_sleeves_id)
            selected_bottom_pattern =get_object_or_404(BottomPattern, pk=bottom_pattern_id)
            selected_fabric_pattern =get_object_or_404(BottomPattern, pk=top_fabric_id)

            # Retrieve the associated DressType
            selected_dress_type = selected_top_pattern.dress_type

            # Append DressType to the selected_patterns list
            selected_patterns.append(selected_dress_type.dress_type)
            selected_pattern_id.append(selected_dress_type.dress_type)

            # Calculate the total price based on the selected patterns
            total_price = (
                selected_dress_type.price +
                selected_top_pattern.price +
                selected_neck_pattern.price +
                selected_sleeves_pattern.price +
                selected_bottom_pattern.price+
                selected_fabric_pattern.price
            )

        except (ValueError, TopPattern.DoesNotExist):
            selected_patterns.append('TopPattern Not Found')
            total_price = 0  # Set a default value in case of errors
            
            
        selected_patterns_str = ','.join(selected_patterns)
        selected_pattern_id_str = ','.join(map(str, selected_pattern_id))
        total_price_str = str(total_price)    
        total_price_str = str(total_price)
        selected_patterns_encoded = quote(selected_patterns_str)
        selected_pattern_id_encoded = quote(selected_pattern_id_str)
        total_price_encoded = quote(total_price_str)

        # Render the template with the selected pattern names and total price
        return redirect('display_selected_patterns', selected_patterns=selected_patterns_encoded, selected_pattern_id=selected_pattern_id_encoded, total_price=total_price_encoded)
    else:
        # Handle the case when the request method is not POST (e.g., redirect or show an error)
        return HttpResponse("Invalid Request")



def display_selected_patterns(request, selected_patterns, selected_pattern_id, total_price):
    # Replace these with your actual data
    selected_patterns_decoded = unquote(selected_patterns).split(',')
    selected_pattern_id_decoded = unquote(selected_pattern_id).split(',')
    total_price_decoded = unquote(total_price)
    
    selected_patterns_list = selected_patterns_decoded
    selected_pattern_id_list = selected_pattern_id_decoded  # Correct variable name
    
    

    # Create dictionaries for selected patterns and pattern IDs
    selected_patterns_dict = {
        'fabric': selected_patterns_list[0],
        'neck': selected_patterns_list[1],
        'top': selected_patterns_list[2],
        'sleeves': selected_patterns_list[3],
        'bottom': selected_patterns_list[4],
        'dresstype':selected_patterns_list[5]
    }

    selected_pattern_id_dict = {
        'fabric_id': selected_pattern_id_list[0],
        'neck_id': selected_pattern_id_list[1],
        'top_id': selected_pattern_id_list[2],
        'sleeves_id': selected_pattern_id_list[3],
        'bottom_id': selected_pattern_id_list[4],
        'dresstype':selected_patterns_list[5]
    }

    # Replace with your actual calculation logic

    context = {
        'selected_patterns': selected_patterns_dict,
        'selected_patterns_id': selected_pattern_id_dict,
        'total_price': total_price_decoded,  # Correct variable name
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
        dresstype = request.POST.get('desstype_id')
        price =request.POST.get('total_price')

        # Get instances of the pattern models using the IDs
        try:
            fabric_pattern = get_object_or_404(Fabric, pk=fabric_id)
            neck_pattern = get_object_or_404(NeckPattern, pk=neck_id)
            top_pattern = get_object_or_404(TopPattern, pk=top_id)
            sleeves_pattern = get_object_or_404(SleevesPattern, pk=sleeves_id)
            bottom_pattern = get_object_or_404(BottomPattern, pk=bottom_id)
            dresstype = get_object_or_404(DressType, pk=dresstype)
            

            # Assuming you have the necessary data to create a Designs object
            user = request.user  # Get the current user

            try:
                # Create the Designs object with the retrieved instances
                design = Designs.objects.create(
                    user=user,
                    dress_type=dresstype,
                    neck_pattern=neck_pattern,
                    sleeves_pattern=sleeves_pattern,
                    bottom_pattern=bottom_pattern,
                    top_pattern=top_pattern,
                    fabric1=fabric_pattern,
                    price= price,
                )
                design.save()

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
    

    
    
    
# order

def order_confirmation_view(request, design_id):
    try:
        # Fetch the design based on the provided design_id
        design = Designs.objects.get(pk=design_id)
        
        # Calculate the total price based on the design's price or any other relevant logic
        total_price = design.price  # You can adjust this based on your requirements
        
        # Pass the design and total_price to the template
        context = {
            'design': design,
            'total_price': total_price,
        }

        return render(request, 'order_confirmation.html', context)

    except Designs.DoesNotExist:
        return HttpResponse("Design not found")
