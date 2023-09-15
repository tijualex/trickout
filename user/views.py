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
from customadmin.models import BottomPattern, Dress, DressType, NeckPattern, SleevesPattern
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
def measurement_sub(request):
    if request.method == 'POST':
        waist = request.POST['waist']
        shoulder = request.POST['shoulder']
        chest = request.POST['chest']
        stomach = request.POST['stomach']
        hips = request.POST['hips']
        gender = request.POST['gender']

        # Create a new measurement associated with the currently authenticated user
        measurement = PersonMeasurement(
            user=request.user,  # Assign the currently authenticated user
            waist=waist,
            shoulder=shoulder,
            chest=chest,
            stomach=stomach,
            hips=hips,
            gender=gender
        )
        measurement.save()

        # Redirect to a success page or another appropriate action
        return redirect('index')

    return render(request, 'design/measurement.html')


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
        

        
        
        # Initialize a list to store selected pattern names
        selected_patterns = []
        
        # Fetch the pattern names from the database and handle errors gracefully
        def get_pattern_name(pattern_str, pattern_model):
            try:
                pattern_id = int(pattern_str)
                selected_pattern = get_object_or_404(pattern_model, pk=pattern_id)
                selected_patterns.append(selected_pattern.name)
            except (ValueError, pattern_model.DoesNotExist):
                selected_patterns.append('Pattern Not Found')
        print(f"selected_neck_pattern: {selected_patterns}")
        get_pattern_name(selected_fabric_pattern_str, Fabric)
        get_pattern_name(selected_neck_pattern_str, NeckPattern)
        get_pattern_name(selected_top_pattern_str, TopPattern)
        get_pattern_name(selected_sleeves_pattern_str, SleevesPattern)
        get_pattern_name(selected_bottom_pattern_str, BottomPattern)
        
        # Calculate the total price (you should have this logic implemented)
        total_price = 100  # Replace with your actual calculation logic
        
        # Render the template with the selected pattern names and total price
        return redirect('display_selected_patterns', selected_patterns=selected_patterns, total_price=total_price)
    else:
        # Handle the case when the request method is not POST (e.g., redirect or show an error)
        return HttpResponse("Invalid Request")


def display_selected_patterns(request, selected_patterns, total_price):
    # Replace these with your actual data
    selected_patterns_list = ast.literal_eval(selected_patterns)
    
    selected_patterns = {
        'fabric': selected_patterns_list[0],
        'neck': selected_patterns_list[1],
        'top': selected_patterns_list[2],
        'sleeves': selected_patterns_list[3],
        'bottom': selected_patterns_list[4],
    }
    total_price = 100  # Replace with your actual calculation logic

    context = {
        
        'selected_patterns': selected_patterns,
        'total_price': total_price,
    }

    return render(request, 'design/confirm_design.html', context)




# dress detail view
class DressDetailView(DetailView):
    model = Dress
    template_name = 'dress_detail.html'  # Create this template for displaying Dress details
    context_object_name = 'dress'  # This will be the variable name in the template