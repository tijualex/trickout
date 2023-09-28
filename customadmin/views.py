# # views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import PersonMeasurement, User, UserProfile
from .models import BottomPattern, Designs, Fabric, NeckPattern, DressType, SleevesPattern, TopPattern


def admin_index(request):
    return render(request,'admin_index.html')







# neck pattern
@login_required
@csrf_exempt
def add_neck_pattern(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            name = request.POST['name']
            image = request.FILES['image']
            dress_type_id = request.POST['dressType']
            price = request.POST['price']

            # Check if the specified DressType exists
            try:
                dress_type = DressType.objects.get(pk=dress_type_id)
            except DressType.DoesNotExist:
                return JsonResponse({'message': 'Invalid DressType'}, status=400)

            # Check if a NeckPattern with the same name and dress type already exists
            existing_pattern = NeckPattern.objects.filter(name=name, dress_type=dress_type).first()
            if existing_pattern:
                return JsonResponse({'message': 'Pattern with the same name and dress type already exists'}, status=400)

            # Continue with saving the new NeckPattern to the database
            neck_pattern = NeckPattern(name=name, image=image, dress_type=dress_type, price=price)
            neck_pattern.save()

            # Redirect to the list_neck_pattern URL upon successful addition
            return redirect('list_neck_pattern')
        except Exception as e:
            # Handle exceptions or validation errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    else:
        # Render the HTML template when it's a GET request
        dress_types = DressType.objects.all()
        return render(request, 'add_neckpattern.html', {'dress_types': dress_types})





def list_neck_pattern(request):
    neck_patterns = NeckPattern.objects.all()
    return render(request, 'neckpattern_grid.html', {'neck_patterns': neck_patterns})


def get_neck_pattern_details(request, pattern_id):
    try:
        pattern = get_object_or_404(NeckPattern, custom_id=pattern_id)
        pattern_data = {
            'name': pattern.name,
            'image_url': pattern.image.url,
            'details': pattern.details,
            'dress_type': pattern.dress_type.dress_type,  # Assuming DressType has a 'name' field
            'price': str(pattern.price),  # Convert DecimalField to string
            'is_active': pattern.is_active,
        }
        return JsonResponse(pattern_data)
    except NeckPattern.DoesNotExist:
        return JsonResponse({'error': 'Pattern not found'}, status=404)
    
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def update_neck_pattern(request, pattern_id):
    if request.method == 'POST':
        pattern = get_object_or_404(NeckPattern, custom_id=pattern_id)
        
        # Update price and is_active
        price = request.POST.get('priceupdate', '0.00')
        print(f"Received price: {price}")  # Debugging: Print received price
        price_decimal = Decimal(price)
        is_active = request.POST.get('is-active-update', False)
        
        # Convert is_active to a Python boolean
        is_active = is_active == 'on'
        print(f"Received is_active: {is_active}")  # Debugging: Print received is_active
        
        pattern.price = price_decimal
        pattern.is_active = is_active
        
        # Update image if provided
        if 'neckPatternImageupdate' in request.FILES:
            print("Image file provided.")  # Debugging: Print if image file provided
            pattern.image = request.FILES['neckPatternImageupdate']
        
        pattern.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



    
    
    
#bottom pattern

@login_required
@csrf_exempt
def add_bottom_pattern(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            name = request.POST['name']
            image = request.FILES['image']
            dress_type_id = request.POST['dressType']
            price = request.POST['price']

            # Check if the specified DressType exists
            try:
                dress_type = DressType.objects.get(pk=dress_type_id)
            except DressType.DoesNotExist:
                return JsonResponse({'message': 'Invalid DressType'}, status=400)

            # Check if a BottomPattern with the same name and dress type already exists
            existing_pattern = BottomPattern.objects.filter(name=name, dress_type=dress_type).first()
            if existing_pattern:
                return JsonResponse({'message': 'Pattern with the same name and dress type already exists'}, status=400)

            # Continue with saving the new BottomPattern to the database
            bottom_pattern = BottomPattern(name=name, image=image, dress_type=dress_type, price=price)
            bottom_pattern.save()

            # Redirect to the list_bottom_pattern URL upon successful addition
            return redirect('list_bottom_pattern')
        except Exception as e:
            # Handle exceptions or validation errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    else:
        # Render the HTML template when it's a GET request
        dress_types = DressType.objects.all()
        return render(request, 'add_bottompattern.html', {'dress_types': dress_types})


def list_bottom_pattern(request):
    bottom_patterns = BottomPattern.objects.all()
    return render(request, 'bottompattern_grid.html', {'bottom_patterns': bottom_patterns})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import BottomPattern

@login_required
def get_bottom_pattern_details(request, pattern_id):
    try:
        pattern = BottomPattern.objects.get(custom_id=pattern_id)
        pattern_data = {
            'name': pattern.name,
            'image_url': pattern.image.url,
            'details': pattern.details,
            'dress_type': pattern.dress_type.dress_type,  # Assuming DressType has a 'name' field
            'price': str(pattern.price),  # Convert DecimalField to string
            'is_active': pattern.is_active,
        }
        return JsonResponse(pattern_data)
    except BottomPattern.DoesNotExist:
        return JsonResponse({'error': 'Pattern not found'}, status=404)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal

from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import BottomPattern

def update_bottom_pattern(request, pattern_id):
    if request.method == 'POST':
        pattern = get_object_or_404(BottomPattern, custom_id=pattern_id)
        
        # Update price and is_active
        price = request.POST.get('priceupdate', '0.00')
        print(f"Received price: {price}")  # Debugging: Print received price
        price_decimal = Decimal(price)
        is_active = request.POST.get('is-active-update', False)
        
        # Convert is_active to a Python boolean
        is_active = is_active == 'on'
        print(f"Received is_active: {is_active}")  # Debugging: Print received is_active
        
        pattern.price = price_decimal
        pattern.is_active = is_active
        
        # Update image if provided
        if 'bottomPatternImageupdate' in request.FILES:
            print("Image file provided.")  # Debugging: Print if image file provided
            pattern.image = request.FILES['bottomPatternImageupdate']
        
        pattern.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# top pattern

@login_required
@csrf_exempt
def add_top_pattern(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            name = request.POST['name']
            image = request.FILES['image']
            dress_type_id = request.POST['dressType']
            price = request.POST['price']

            # Check if the specified DressType exists
            try:
                dress_type = DressType.objects.get(pk=dress_type_id)
            except DressType.DoesNotExist:
                return JsonResponse({'message': 'Invalid DressType'}, status=400)

            # Check if a TopPattern with the same name and dress type already exists
            existing_pattern = TopPattern.objects.filter(name=name, dress_type=dress_type).first()
            if existing_pattern:
                return JsonResponse({'message': 'Pattern with the same name and dress type already exists'}, status=400)

            # Continue with saving the new TopPattern to the database
            top_pattern = TopPattern(name=name, image=image, dress_type=dress_type, price=price)
            top_pattern.save()

            # Redirect to the list_top_pattern URL upon successful addition
            return redirect('list_top_pattern')
        except Exception as e:
            # Handle exceptions or validation errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    else:
        # Render the HTML template when it's a GET request
        dress_types = DressType.objects.all()
        return render(request, 'add_toppattern.html', {'dress_types': dress_types})

    
def list_top_pattern(request):
    top_patterns = TopPattern.objects.all()
    return render(request, 'toppattern_grid.html', {'top_patterns': top_patterns})

def get_top_pattern_details(request, pattern_id):
    try:
        pattern = get_object_or_404(TopPattern, custom_id=pattern_id)
        pattern_data = {
            'name': pattern.name,
            'image_url': pattern.image.url,
            'price': str(pattern.price),  # Convert DecimalField to string
            'is_active': pattern.is_active,
        }
        return JsonResponse(pattern_data)
    except TopPattern.DoesNotExist:
        return JsonResponse({'error': 'Pattern not found'}, status=404)


def update_top_pattern(request, pattern_id):
    if request.method == 'POST':
        pattern = get_object_or_404(TopPattern, custom_id=pattern_id)

        # Update price and is_active
        price = request.POST.get('priceupdate', '0.00')
        print(f"Received price: {price}")  # Debugging: Print received price
        price_decimal = Decimal(price)
        is_active = request.POST.get('is-active-update', False)

        # Convert is_active to a Python boolean
        is_active = is_active == 'on'
        print(f"Received is_active: {is_active}")  # Debugging: Print received is_active

        pattern.price = price_decimal
        pattern.is_active = is_active

        # Update image if provided
        if 'topPatternImageupdate' in request.FILES:
            print("Image file provided.")  # Debugging: Print if image file provided
            pattern.image = request.FILES['topPatternImageupdate']

        pattern.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)







# sleeves
@login_required
@csrf_exempt
def add_sleeves_pattern(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            name = request.POST['name']
            image = request.FILES['image']
            dress_type_id = request.POST['dressType']
            price = request.POST['price']

            # Check if the specified DressType exists
            try:
                dress_type = DressType.objects.get(pk=dress_type_id)
            except DressType.DoesNotExist:
                return JsonResponse({'message': 'Invalid DressType'}, status=400)

            # Check if a SleevesPattern with the same name and dress type already exists
            existing_pattern = SleevesPattern.objects.filter(name=name, dress_type=dress_type).first()
            if existing_pattern:
                return JsonResponse({'message': 'Pattern with the same name and dress type already exists'}, status=400)

            # Continue with saving the new SleevesPattern to the database
            sleeves_pattern = SleevesPattern(name=name, image=image, dress_type=dress_type, price=price)
            sleeves_pattern.save()

             # Redirect to the sleeves_grid URL upon successful addition
            return redirect('list_sleeves_pattern')
        except Exception as e:
            # Handle exceptions or validation errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    else:
        # Render the HTML template when it's a GET request
        dress_types = DressType.objects.all()
        return render(request, 'add_sleevespattern.html', {'dress_types': dress_types})
    
def list_sleeves_pattern(request):
    sleeves_patterns = SleevesPattern.objects.all()
    return render(request, 'sleevespattern_grid.html', {'sleeves_patterns': sleeves_patterns})


def get_sleeves_pattern_details(request, pattern_id):
    try:
        pattern = get_object_or_404(SleevesPattern, custom_id=pattern_id)
        pattern_data = {
            'name': pattern.name,
            'image_url': pattern.image.url,
            'details': pattern.details,
            'dress_type': pattern.dress_type.dress_type,  # Assuming DressType has a 'name' field
            'price': str(pattern.price),  # Convert DecimalField to string
            'is_active': pattern.is_active,
        }
        return JsonResponse(pattern_data)
    except SleevesPattern.DoesNotExist:
        return JsonResponse({'error': 'Pattern not found'}, status=404)

def update_sleeves_pattern(request, pattern_id):
    try:
        pattern = get_object_or_404(SleevesPattern, custom_id=pattern_id)

        # Update price and is_active
        price = request.POST.get('priceupdate', '0.00')
        price_decimal = Decimal(price)
        is_active = request.POST.get('is-active-update', False)

        # Convert is_active to a Python boolean
        is_active = is_active == 'on'

        pattern.price = price_decimal
        pattern.is_active = is_active

        # Update image if provided
        if 'sleevesPatternImageupdate' in request.FILES:
            pattern.image = request.FILES['sleevesPatternImageupdate']

        pattern.save()
        return JsonResponse({'success': True})
    except SleevesPattern.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pattern not found'}, status=404)


# fabric
@login_required
@csrf_exempt
def add_fabric(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            name = request.POST['name']
            image = request.FILES['fabric_image']
            price = request.POST['price']

            # Check if a Fabric with the same name already exists
            existing_fabric = Fabric.objects.filter(name=name).first()
            if existing_fabric:
                return JsonResponse({'message': 'Fabric with the same name already exists'}, status=400)

            # Continue with saving the new Fabric to the database
            fabric = Fabric(name=name, fabric_image=image, price=price)
            fabric.save()

            # Redirect to the fabric_grid URL upon successful addition
            return redirect('fabric_grid')
        except Exception as e:
            # Handle exceptions or validation errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    else:
        # If it's not a POST request, simply render the HTML page
        return render(request, 'add_fabric.html')

def fabric_grid(request):
    fabrics = Fabric.objects.all()
    return render(request, 'fabric_grid.html', {'fabrics': fabrics})

@csrf_exempt
def soft_delete_fabric(request, fabric_id):
    try:
        fabric = Fabric.objects.get(pk=fabric_id)
        fabric.soft_delete()
        return JsonResponse({'message': 'Fabric deleted successfully'})
    except Fabric.DoesNotExist:
        return JsonResponse({'error': 'Fabric not found'}, status=404)


def get_fabric_details(request, fabric_id):
    fabric = get_object_or_404(Fabric, custom_id=fabric_id)
    fabric_data = {
        'name': fabric.name,
        'details': fabric.details,
        'price': float(fabric.price),
        'is_active': fabric.is_active,
        'image_url': fabric.fabric_image.url,
    }
    return JsonResponse(fabric_data)

@csrf_exempt  # Add this decorator to handle POST requests without CSRF token
def update_fabric(request, fabric_id):
    if request.method == 'POST':
        fabric = get_object_or_404(Fabric, custom_id=fabric_id)
        
        # Get the updated details from the POST request
        details = request.POST.get('detailsupdate')
        price = request.POST.get('priceupdate')
        is_active = request.POST.get('is-active-update')
        
        # Perform validation and update the fabric instance
        try:
            price = float(price)
            fabric.details = details
            fabric.price = price
            fabric.is_active = is_active == 'on'
            fabric.save()
            return JsonResponse({'success': True})
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid price'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})



# dress type

@login_required
@csrf_exempt
def add_dress_type(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            dress_type_name = request.POST['dress_type']
            image = request.FILES['image']  # Get the uploaded image file
            dress_type_price = request.POST['price']

            # Check if a DressType with the same name already exists
            existing_dress_type = DressType.objects.filter(dress_type=dress_type_name).first()
            if existing_dress_type:
                return JsonResponse({'message': 'DressType with the same name already exists'}, status=400)

            # Continue with saving the new DressType to the database
            dress_type = DressType(dress_type=dress_type_name, image=image,price=dress_type_price)
            dress_type.save()

            # Redirect to the dress_type_grid URL upon successful addition
            return redirect('list_dress_type')
        except Exception as e:
            # Handle exceptions or validation errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    else:
        # If it's not a POST request, simply render the HTML page
        return render(request, 'add_dresstype.html')

    
def list_dress_type(request):
    dress_types = DressType.objects.all()
    return render(request, 'dresstype_grid.html', {'dress_types': dress_types})





# users design

from .models import Designs  # Import your models here

def users_design(request):
    # Retrieve a list of Design objects
    designs = Designs.objects.all()

    context = {
        'designs': designs,
    }

    return render(request, 'users_design.html', context)

def measurement_display(request, measurement_id):
    # Retrieve the design object based on the measurement ID
    try:
        measurement = PersonMeasurement.objects.get(pk=measurement_id)
    except PersonMeasurement.DoesNotExist:
        # Handle the case when the measurement does not exist
        measurement = None

    context = {
        'measurement': measurement,
    }

    return render(request, 'measurement_view.html', context)


# users

# users
@login_required
def list_users(request):
    users = User.objects.all()
    # Fetch all users from the User model
    return render(request, "users_list.html", {"users": users})

def show_user_designs(request, user_id):
    # Retrieve the user's profile based on the user_id or handle 404 error
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    # Retrieve the designs associated with the user's profile
    designs = Designs.objects.filter(user=user_profile.user)

    context = {
        'user_profile': user_profile,
        'designs': designs,
    }

    return render(request, 'show_user_designs.html', context)



def show_user_designs(request, user_id):
    try:
        # Retrieve the user object based on the user_id
        user = User.objects.get(pk=user_id)

        # Retrieve the designs associated with the user
        user_designs = Designs.objects.filter(user=user)

        context = {
            'user': user,
            'user_designs': user_designs,
        }

        return render(request, 'user_designs_individual.html', context)

    except User.DoesNotExist:
        # Handle the case when the user does not exist
        return render(request, 'user_not_found.html')


from  user.models import Order
#orders
def order_list(request):
    orders = Order.objects.select_related('design').all()
    return render(request, 'order_list.html', {'orders': orders})


# views.py
from django.http import JsonResponse
from user.models import Order

def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')

        try:
            order = Order.objects.get(pk=order_id)
            order.order_status = new_status
            order.save()
            return JsonResponse({'success': True, 'new_status': new_status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
