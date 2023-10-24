from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customadmin.models import Designs
from django.contrib.auth.models import User
from user.models import PersonMeasurement, User
from customadmin.models import BottomPattern, Designs, Fabric, NeckPattern, DressType, SleevesPattern, TopPattern
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal

def index_designer(request):
    return render(request, 'designer_dash/index_designer.html')

#user
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


from  user.models import Order, ShippingAddress
#orders
from customadmin.models import UserRole  # Import UserRole model

def order_list(request):
    # Ensure the user is authenticated and has the designer role
    if request.user.is_authenticated and UserRole.objects.filter(user=request.user, role='designer').exists():
        designer_id = request.user.id
        orders = Order.objects.filter(designer_id=designer_id)

        # Filtering logic
        status_filter = request.GET.get('status', None)
        if status_filter in ['processing', 'shipped', 'delivered']:
            orders = orders.filter(order_status=status_filter)

        # Sorting logic
        sort_by = request.GET.get('sort_by', 'order_date')
        orders = orders.order_by(sort_by)

        return render(request, 'designer_dash/order_list.html', {'orders': orders})
    else:
        # Handle the case where the user is not authenticated or not a designer
        return render(request, 'error.html', {'error_message': 'Access denied. You do not have permission to view this page.'})


# patterns 
def view_patterns(request):
    return render(request, 'designer_dash/patterns.html')



# address
from django.shortcuts import render
from user.models import ShippingAddress

def shipping_address_details(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        shipping_address = ShippingAddress.objects.get(user=order.user)
        context = {
            'shipping_address': shipping_address
        }
        return render(request, 'designer_dash/shipping_adress.html', context)
    except (Order.DoesNotExist, ShippingAddress.DoesNotExist):
        # Handle the case where the order or shipping address does not exist
        return render(request, 'error.html', {'error_message': 'Order or shipping address not found.'})



#design
from django.shortcuts import render, get_object_or_404
from customadmin.models import Designs
from user.models import PersonMeasurement


def design_details(request, design_id):
    design = Designs.objects.get(design_id=design_id)
    
    return render(request, 'designer_dash/design_details.html', {'design': design})


def measurement_details(request, design_id):
    # Retrieve the design object based on the measurement ID
    try:
        measurement = PersonMeasurement.objects.get(design_id=design_id)
    except PersonMeasurement.DoesNotExist:
        # Handle the case when the measurement does not exist
        measurement = None

    context = {
        'measurement': measurement,
    }
    return render(request, 'designer_dash/measurement_view.html', context)




# neckapttern

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
        return render(request, 'designer_dash/add_neckpattern.html', {'dress_types': dress_types})

def get_neck_pattern_details(request, pattern_id):
    try:
        pattern = get_object_or_404(NeckPattern, neck_id=pattern_id)
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
        pattern = get_object_or_404(NeckPattern, neck_id=pattern_id)
        
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

def list_neckpattern(request):
    neck_patterns = NeckPattern.objects.all()
    return render(request, 'designer_dash/neckpattern_grid.html', {'neck_patterns': neck_patterns})

# bottompattern

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
        return render(request, 'designer_dash/add_bottompattern.html', {'dress_types': dress_types})


def list_bottompattern(request):
    bottom_patterns = BottomPattern.objects.all()
    return render(request, 'designer_dash/bottompattern_grid.html', {'bottom_patterns': bottom_patterns})


@login_required
def get_bottom_pattern_details(request, pattern_id):
    try:
        pattern = BottomPattern.objects.get(bottom_id=pattern_id)
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




def update_bottom_pattern(request, pattern_id):
    if request.method == 'POST':
        pattern = get_object_or_404(BottomPattern, bottom_id=pattern_id)
        
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
        return render(request, 'designer_dash/add_toppattern.html', {'dress_types': dress_types})

    
def list_toppattern(request):
    top_patterns = TopPattern.objects.all()
    return render(request, 'designer_dash/toppattern_grid.html', {'top_patterns': top_patterns})

def get_top_pattern_details(request, pattern_id):
    try:
        pattern = get_object_or_404(TopPattern, top_id=pattern_id)
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
        pattern = get_object_or_404(TopPattern, top_id=pattern_id)

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
        return render(request, 'designer_dash/add_sleevespattern.html', {'dress_types': dress_types})
    
def list_sleevespattern(request):
    sleeves_patterns = SleevesPattern.objects.all()
    return render(request, 'designer_dash/sleevespattern_grid.html', {'sleeves_patterns': sleeves_patterns})


def get_sleeves_pattern_details(request, pattern_id):
    try:
        pattern = get_object_or_404(SleevesPattern, sleeve_id=pattern_id)
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
        pattern = get_object_or_404(SleevesPattern, sleeve_id=pattern_id)

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
        return render(request, 'designer_dash/add_fabric.html')

def fabric_list(request):
    fabrics = Fabric.objects.all()
    return render(request, 'designer_dash/fabric_grid.html', {'fabrics': fabrics})

@csrf_exempt
def soft_delete_fabric(request, fabric_id):
    try:
        fabric = Fabric.objects.get(pk=fabric_id)
        fabric.soft_delete()
        return JsonResponse({'message': 'Fabric deleted successfully'})
    except Fabric.DoesNotExist:
        return JsonResponse({'error': 'Fabric not found'}, status=404)


def get_fabric_details(request, fabric_id):
    fabric = get_object_or_404(Fabric, fabric_id=fabric_id)
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
        fabric = get_object_or_404(Fabric, fabric_id=fabric_id)
        
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
        return render(request, 'designer_dash/add_dresstype.html')

    
def list_dress_type(request):
    dress_types = DressType.objects.all()
    return render(request, 'designer_dash/dresstype_grid.html', {'dress_types': dress_types})


