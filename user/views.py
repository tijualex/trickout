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
from .models import Order, PersonMeasurement, ShippingAddress, UserProfile 
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
        'neck': selected_patterns_list[2],
        'top': selected_patterns_list[1],
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
            fabric_pattern = get_object_or_404(Fabric, pk=fabric_id)
            neck_pattern = get_object_or_404(NeckPattern, pk=neck_id)
            top_pattern = get_object_or_404(TopPattern, pk=top_id)
            sleeves_pattern = get_object_or_404(SleevesPattern, pk=sleeves_id)
            bottom_pattern = get_object_or_404(BottomPattern, pk=bottom_id)
            dresstype = get_object_or_404(DressType, pk=dresstype_id)
            
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


from .models import Designs, ShippingAddress, Order
from django.shortcuts import render, redirect, HttpResponse
from .models import Designs, Order, ShippingAddress

# order_shipping

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Designs, ShippingAddress, Order

def order_shipping(request):
    if request.method == 'POST':
        # Extract data from the form
        recipient_name = request.POST.get('recipient_name')
        address = request.POST.get('address')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        design_id = request.POST.get('design')
        
        # Get the design price from the Designs model
        try:
            design = Designs.objects.get(pk=design_id)
        except Designs.DoesNotExist:
            # Handle the case where the design with the given ID does not exist
            # You might want to display an error message or redirect to an error page.
            return HttpResponse("Design not found")

        # Calculate the total price based on the design price
        total_price = design.price  # You can perform additional calculations if needed
        
        # Get the user ID
        user_id = request.user.id

        # Create ShippingAddress instance
        shipping_address = ShippingAddress.objects.create(
            user_id=user_id,
            recipient_name=recipient_name,
            address_line1=address,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        )
        shipping_address.save()

        # Create Order instance with the calculated total_price
        order = Order.objects.create(
            user_id=user_id,
            design=design,
            total_price=total_price  # Assign the calculated total_price to the order
        )
        
        # Redirect to the 'payment_confirm' view with the order ID
        return redirect('payment_confirm', order_id=order.order_id)

    else:
        # Handle GET request or other cases
        return render(request, 'error.html')

# payment

import razorpay
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment
from django.contrib.auth.decorators import login_required

# Initialize Razorpay client with API Keys
import razorpay
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Order, Payment
from django.contrib.auth.decorators import login_required

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

# Function to create and display the payment page
@login_required
def payment_confirm(request, order_id):
    # Retrieve the order based on the order_id
    order = get_object_or_404(Order, order_id=order_id)

    # Check if the order is already paid
    if order.payment_status:
        return render(request, 'payment_already_paid.html')

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
    razorpay_order_id = razorpay_order['id']

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


# Function to handle Razorpay payment response
@csrf_exempt
def paymenthandler(request):
    # Only accept POST request.
    if request.method == "POST":
        try:
            # Get the required parameters from the POST request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)

            if result is not None:
                # If signature verification fails.
                return render(request, 'paymentfail.html')

            # Signature verification succeeded, proceed to capture payment.
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
            amount = int(order.total_price * 100)  # Convert total_price to paisa

            try:
                # Capture the payment
                razorpay_client.payment.capture(payment_id, amount)

                # Create a Payment record in your database
                user = request.user
                payment = Payment(user=user, order=order, payment_id=payment_id, amount=amount)
                payment.save()

                # Update the order's payment status
                order.payment_status = True
                order.save()

                # Render a success page on successful capture of payment
                return render(request, 'paymentsuccess.html')
            except Exception as e:
                # If there is an error while capturing payment.
                return render(request, 'paymentfail.html')
        except Exception as e:
            # If we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # If other than POST request is made.
        return HttpResponseBadRequest()
