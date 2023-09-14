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







def measurement(request):
    return render(request,'mesurement.html')

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



@login_required
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

    return render(request, 'measurement_form.html')


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


def dress_detail(request, dress_type_id):
    dress_type = get_object_or_404(DressType, id=dress_type_id)
    context = {
        'dress_type': dress_type,
    }
    return render(request, 'dress_detail.html', context)







# dress detail view
class DressDetailView(DetailView):
    model = Dress
    template_name = 'dress_detail.html'  # Create this template for displaying Dress details
    context_object_name = 'dress'  # This will be the variable name in the template