from decimal import Decimal
from urllib.parse import quote, unquote
from django.http import HttpResponseBadRequest, JsonResponse
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
from requests import request
from .models import Order, PersonMeasurement, ShippingAddress, UserProfile 
from customadmin.models import BottomPattern, Designs, DressType, NeckPattern, SleevesPattern
from customadmin.models import Fabric, TopPattern,UserRole  # Import your Fabric model
 

# Replace 'User' with your custom user model
User = get_user_model()

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.user.is_authenticated:
        # User is already authenticated, redirect to the desired page (e.g., 'index')
        user_role = UserRole.objects.get(user=request.user)
        if user_role.role == 'admin':
            return redirect('admin_index')
        elif user_role.role == 'designer':
            return redirect('index_designer')
        else:
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
            user_role = UserRole.objects.get(user=user)
            if user_role.role == 'admin':
                return redirect('admin_index')
            elif user_role.role == 'designer':
                return redirect('index_designer')
            else:
                return redirect('index')
        else:
            # Invalid login credentials, display an error message
            messages.error(request, "Invalid Login")
            return render(request, 'login.html')

    return render(request, 'login.html')









    

    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

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

                # Assign default role to the new user
                UserRole.objects.create(user=user, role='user')  # 'user' is the default role

                subject = 'Your account has been created'
                message = 'Your account has been created successfully.'
                from_email = settings.EMAIL_HOST_USER  # Your sender email address
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list)

                return redirect('login_view')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
    return render(request, 'signup.html')









from django.shortcuts import render, redirect



def index(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's role (assuming the role is stored in the user profile or User model)
        user_role = request.user.userrole.role  # Adjust this based on your user profile or User model setup
        
        # Redirect based on user roles
        if user_role == 'admin':
            # If the user is an admin, redirect to the admin dashboard or any other desired page
            return redirect('admin_index')  # Replace 'admin_index' with the appropriate URL name for the admin dashboard
        elif user_role == 'designer':
            # If the user is a designer, redirect to the designer index page
            return redirect('index_designer')  # Replace 'index_designer' with the appropriate URL name for the designer index page
        else:
            # For other roles or if the role is not specified, display the regular index page
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

from django.http import JsonResponse

def pattern_details(request, pattern_id, pattern_type):
    # Determine the model based on pattern_type
    if pattern_type == 'fabric':
        pattern_model = Fabric
    elif pattern_type == 'neckpattern':
        pattern_model = NeckPattern
    elif pattern_type == 'toppattern':
        pattern_model = TopPattern
    elif pattern_type == 'sleevespattern':
        pattern_model = SleevesPattern
    elif pattern_type == 'bottompattern':
        pattern_model = BottomPattern
    else:
        # Handle other pattern types or invalid pattern types as needed
        return JsonResponse({'error': 'Invalid pattern type'}, status=400)

    # Get the pattern option based on pattern_id and pattern_model
    pattern_option = get_object_or_404(pattern_model, pk=pattern_id)

    # Prepare pattern details to be sent as JSON response
    pattern_details = {
        'name': pattern_option.name,
        'image_url': pattern_option.image.url,  # Assuming the image field is named 'image'
        # Include other pattern details if necessary
    }

    # Return pattern details as JSON response
    return JsonResponse(pattern_details)



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
        
        pattern_id = int(selected_fabric_pattern_str)
        selected_pattern = get_object_or_404(Fabric, pk=pattern_id)
        selected_pattern_id.append(selected_pattern.fabric_id)
        selected_patterns.append(selected_pattern.name)
        
        pattern_id = int(selected_top_pattern_str)
        selected_pattern = get_object_or_404(TopPattern, pk=pattern_id)
        selected_pattern_id.append(selected_pattern.top_id)
        selected_patterns.append(selected_pattern.name)
        
        pattern_id = int(selected_neck_pattern_str)
        selected_pattern = get_object_or_404(NeckPattern, pk=pattern_id)
        selected_pattern_id.append(selected_pattern.neck_id)
        selected_patterns.append(selected_pattern.name)
        
        pattern_id = int(selected_sleeves_pattern_str)
        selected_pattern = get_object_or_404(SleevesPattern, pk=pattern_id)
        selected_pattern_id.append(selected_pattern.sleeve_id)
        selected_patterns.append(selected_pattern.name)

        pattern_id = int(selected_bottom_pattern_str)
        selected_pattern = get_object_or_404(BottomPattern, pk=pattern_id)
        selected_pattern_id.append(selected_pattern.bottom_id)
        selected_patterns.append(selected_pattern.name)
       

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
            selected_fabric_pattern =get_object_or_404(Fabric, pk=top_fabric_id)

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
    selected_patterns_decoded = unquote(selected_patterns).split(',')
    selected_pattern_id_decoded = unquote(selected_pattern_id).split(',')
    total_price_decoded = unquote(total_price)
    fabric_id = selected_pattern_id_decoded[0]
    neck_id = selected_pattern_id_decoded[2]
    top_id = selected_pattern_id_decoded[1]
    sleeves_id = selected_pattern_id_decoded[3]
    bottom_id = selected_pattern_id_decoded[4]
    dresstype = selected_pattern_id_decoded[5]

    # Retrieve selected pattern objects from the database
    fabric_pattern = Fabric.objects.get(fabric_id=fabric_id)
    neck_pattern = NeckPattern.objects.get(neck_id=neck_id)
    top_pattern = TopPattern.objects.get(top_id=top_id)
    sleeve_pattern = SleevesPattern.objects.get(sleeve_id=sleeves_id)
    bottom_pattern = BottomPattern.objects.get(bottom_id=bottom_id)
    dress_type = DressType.objects.get(dress_type=dresstype)

    context = {
        'selected_patterns': {
            'fabric': fabric_pattern,
            'neck': neck_pattern,
            'top': top_pattern,
            'sleeves': sleeve_pattern,
            'bottom': bottom_pattern,
            'dress_type': dress_type,
        },
        'total_price': total_price_decoded,
    }

    return render(request, 'design/confirm_design.html', context)

import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings







def create_design(request):
    if request.method == 'POST':
        # Retrieve the selected patterns and dress type from the form data
        fabric_id = request.POST.get('fabric_id')
        neck_id = request.POST.get('neck_id')
        top_id = request.POST.get('top_id')
        sleeves_id = request.POST.get('sleeves_id')
        bottom_id = request.POST.get('bottom_id')
        dresstype_id = request.POST.get('dresstype_id')  # corrected field name
        total_price = request.POST.get('total_price')    # corrected field name

        # Get instances of the pattern models using the IDs
        try:
            fabric_id = get_object_or_404(Fabric, pk=fabric_id)
            neck_id = get_object_or_404(NeckPattern, pk=neck_id)
            top_id = get_object_or_404(TopPattern, pk=top_id)
            sleeve_id = get_object_or_404(SleevesPattern, pk=sleeves_id)
            bottom_id = get_object_or_404(BottomPattern, pk=bottom_id)
            dresstype = get_object_or_404(DressType, pk=dresstype_id)
            
            # Assuming you have the necessary data to create a Designs object
            user = request.user  # Get the current user

            try:
                # Create the Designs object with the retrieved instances
                design = Designs.objects.create(
                    user=user,
                    dress_type=dresstype,
                    neck_id=neck_id,
                    sleeve_id=sleeve_id,
                    bottom_id=bottom_id,
                    top_id=top_id,
                    fabric_id=fabric_id,
                    price=total_price,  # corrected field name
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



from django.shortcuts import get_object_or_404
from .models import ShippingAddress

def order_confirmation_view(request, design_id):
    try:
        # Fetch the design based on the provided design_id
        design = Designs.objects.get(pk=design_id)

        # Fetch the current user's addresses
        user_addresses = ShippingAddress.objects.filter(user=request.user)

        # Calculate the total price based on the design's price or any other relevant logic
        total_price = design.price  # You can adjust this based on your requirements

        # Pass the design, total_price, and user_addresses to the template
        context = {
            'design': design,
            'total_price': total_price,
            'user_addresses': user_addresses,
        }

        return render(request, 'order_confirmation.html', context)

    except Designs.DoesNotExist:
        return HttpResponse("Design not found")

# order_shipping


def add_address(request):
    if request.method == 'POST':
        # Extract data from the form
        design_id=request.POST.get('design')
        recipient_name = request.POST.get('recipient_name')
        address_line1 = request.POST.get('address')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        # Get the user ID
        user_id = request.user.id

        # Create ShippingAddress instance
        ShippingAddress.objects.create(
            user_id=user_id,
            recipient_name=recipient_name,
            address_line1=address_line1,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        )

        # Redirect to the same page or any other appropriate page
        return redirect('order_confirmation_view',design_id)

    # Handle GET request or other cases
    return render(request, 'error.html')


from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from .models import Order
import razorpay
from django.conf import settings



import razorpay
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Designs, Order
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
from django.db import transaction

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
import razorpay
from django.conf import settings
from .models import Order, Designs, ShippingAddress
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

from customadmin.models import Designs, UserRole
from user.models import ShippingAddress, Order   # Import the UserRole model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, Designs, ShippingAddress
from django.contrib.auth.decorators import login_required # Import your Razorpay client instance
import random
@login_required
@csrf_exempt
@transaction.atomic
@login_required
def create_order(request):
    if request.method == 'POST':
        # Extract data from the request
        design_id = request.POST.get('design')
        design = get_object_or_404(Designs, pk=design_id)
        delivery_address_id = request.POST.get('selected_address')
        delivery_address = get_object_or_404(ShippingAddress, pk=delivery_address_id)
        amount = int(design.price * 100)  # Razorpay accepts amount in paise, so multiply by 100

        try:
            # Retrieve all active designers
            designers = User.objects.filter(userrole__role='designer', is_active=True)

            # Randomly select a designer from the list
            if designers.exists():
                selected_designer = random.choice(designers)
            else:
                # Handle the case where there are no designers available
                return render(request, 'error.html', {'error_message': 'No designers available for assignment.'})

            # Create a Razorpay order
            order = razorpay_client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })

            # Save the Razorpay order ID in your database
            razorpay_order_id = order['id']

            # Create an Order instance in your database with the selected designer
            order_instance = Order.objects.create(
                user=request.user,
                design=design,
                total_price=design.price,
                address_id=delivery_address,
                razorpay_order_id=razorpay_order_id,
                designer_id=selected_designer
            )

            # Redirect to the payment confirmation page with the order_id
            return redirect('payment_confirm', order_id=order_instance.order_id)

        except Exception as e:
            # Handle exceptions, log the error, and redirect the user to an error page
            print("Error:", str(e))
            return render(request, 'error.html', {'error_message': 'An error occurred while processing your order.'})

    else:
        # Handle invalid requests (GET requests, etc.)
        return render(request, 'error.html', {'error_message': 'Invalid request method'})


@login_required
@csrf_exempt
def payment_confirm(request, order_id):
    # Retrieve the order based on the order_id
    order = get_object_or_404(Order, order_id=order_id)

    # Check if the order is already paid
    # if order.payment_status:
    #     return render(request, 'error.html', {'error_message': 'Already paid.'})

    # Get the total_price from the order
    total_price = order.total_price

    # Razorpay integration code goes here
    currency = 'INR'
    amount = int(total_price * 100)  # Convert total_price to paisa (assuming price is in rupees)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture='0')
    )

    # Extract the order id of the newly created order
    razorpay_order_id = order.razorpay_order_id
    

    # Define the callback URL
    callback_url = '/paymenthandler/'  # Update this URL to your actual payment handler

    # Pass these details to the frontend
    context = {
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_API_KEY,  # Use API Key, not Key ID
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment.html', context)
@login_required
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        print("Received parameters:")
        print("Razorpay Order ID:", razorpay_order_id)
        print("Razorpay Payment ID:", razorpay_payment_id)
        print("Razorpay Signature:", razorpay_signature)


        # Your Razorpay API key and secret
        razorpay_key_id =  settings.RAZORPAY_API_KEY
        
        razorpay_key_secret = settings.RAZORPAY_API_SECRET

        # Initialize Razorpay client
        razorpay_client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict, razorpay_signature)
        except Exception as e:
            # Signature verification failed
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

            order.payment_id = razorpay_payment_id
            order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
            order.save()

            # Redirect to the user's orders page after successful payment
            return redirect('myorders')

        # Fetch the order from your database based on razorpay_order_id
        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

        # Ensure the order is pending and payment is not already successful
        if order.payment_status != Order.PaymentStatusChoices.PENDING:
            return HttpResponseBadRequest("Invalid order status")

        # Convert total price to paise
        amount = int(order.total_price * 100)

        try:
            # Capture the payment amount
            razorpay_client.payment.capture(razorpay_payment_id, amount)

            # Update the order with payment ID and change status to "Successful"
            order.payment_id = razorpay_payment_id
            order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
            order.save()

            # Redirect to the user's orders page after successful payment
            return redirect('myorders')

        except Exception as e:
            # Handle payment capture failure or other exceptions
            return HttpResponseBadRequest("Payment capture failed")

    return HttpResponseBadRequest("Invalid request method")


@login_required
def myorders(request):
    # Retrieve orders for the currently logged-in user and sort them in reverse order
    user_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    
    context = {
        'orders': user_orders,
    }
    
    return render(request, 'my_orders.html', context)


# my designs
def my_designs(request):
    # Retrieve orders for the currently logged-in user
    user_designs =Designs.objects.filter(user=request.user)
    
    context = {
        'designs': user_designs,
    }
    
    return render(request, 'my_designs.html', context)


def view_design(request, design_id):
    design = Designs.objects.get(design_id=design_id)
    
    return render(request, 'view_design.html', {'design': design})



#invoice download 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from reportlab.platypus.doctemplate import Indenter
from reportlab.platypus.flowables import KeepTogether
from django.http import HttpResponse
from django.http import FileResponse
from .models import Order

def export_order_details_pdf(request, order_id):
    # Fetch the specific order from the database
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # Define table header and data for the specific order
    data = [
        ["Order ID", "Order Date", "Order Time", "Amount Payable", "Order Status", "Payment Status"],
        [
            order.order_id,
            order.order_date.strftime("%Y-%m-%d"),
            order.order_date.strftime("%H:%M:%S"),
            order.total_price,
            order.get_order_status_display(),
            order.get_payment_status_display(),
    
        ]
    ]

    # Create a buffer and a PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add the Trickout heading
    styles = getSampleStyleSheet()
    trickout_heading_style = ParagraphStyle(
        "TrickoutHeading",
        parent=styles["Heading1"],
        alignment=1  # 0=Left, 1=Center, 2=Right
    )
    trickout_heading = Paragraph("Trickout", trickout_heading_style)
    elements.append(trickout_heading)

    # Add the 'Details of the Order' heading
    details_heading_style = ParagraphStyle(
        "DetailsHeading",
        parent=styles["Heading2"],
        alignment=1  # 0=Left, 1=Center, 2=Right
    )
    details_heading = Paragraph("Order Details", details_heading_style)
    elements.append(details_heading)

    # Add a line space for better separation
    elements.append(Spacer(1, 12))

    # Define column widths for the table
    col_widths = [80, 80, 80, 80, 80, 80, 80]  # Adjust widths as needed

    # Define table style (same as before)
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])

    # Create the table with specified column widths and apply the style
    table = Table(data, colWidths=col_widths)
    table.setStyle(style)

    # Wrap the table in KeepTogether to ensure it doesn't break across pages
    elements.append(KeepTogether([table]))

    # Build the PDF and prepare the response
    doc.build(elements)
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename=f'order_{order.order_id}_details.pdf')
    return response
