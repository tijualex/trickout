# # views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BottomPattern, Fabric, NeckPattern, DressType, SleevesPattern, TopPattern


def admin_index(request):
    return render(request,'admin_index.html')







# neck pattern
@login_required
@csrf_exempt
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
def update_bottom_pattern(request, bottom_pattern_id):
    if request.method == 'POST':
        # Get the bottom pattern instance based on the bottom pattern ID
        bottom_pattern = get_object_or_404(BottomPattern, custom_id=bottom_pattern_id)

        # Process the form data
        bottom_pattern.price = request.POST.get('priceupdate')

        # Set the is_active field directly to a boolean value
        bottom_pattern.is_active = request.POST.get('is-active-update') == 'on'

        # Check if a new bottom pattern image is provided
        if request.FILES.get('bottomPatternImageupdate'):
            bottom_pattern.image = request.FILES['bottomPatternImageupdate']

        # Save the updated bottom pattern
        bottom_pattern.save()

        # Return a JSON response indicating success or redirect to a different URL
        return redirect('list_bottom_pattern')

    # Handle GET requests or other HTTP methods
    return JsonResponse({'message': 'Invalid request method'}, status=400)







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


from django.shortcuts import render, get_object_or_404, redirect
from .models import TopPattern

def update_top_pattern(request, top_pattern_id):
    top_pattern = get_object_or_404(TopPattern, pk=top_pattern_id)

    if request.method == 'POST':
        # Handle form submission here
        price = request.POST.get('price', top_pattern.price)
        is_active = request.POST.get('is_active', top_pattern.is_active)

        # Handle image file upload if needed
        if 'image' in request.FILES:
            image = request.FILES['image']
            top_pattern.image = image

        # Update the top pattern fields
        top_pattern.price = price
        top_pattern.is_active = is_active

        # Save the updated pattern
        top_pattern.save()

        # Optionally, you can return a success message as JSON
        return JsonResponse({'message': 'Top Pattern updated successfully'})

    # Render the update form for top patterns
    return render(request, 'update_top_pattern.html', {'top_pattern': top_pattern})







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


# dress type

@login_required
@csrf_exempt
def add_dress_type(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            dress_type_name = request.POST['dress_type']
            image = request.FILES['image']  # Get the uploaded image file

            # Check if a DressType with the same name already exists
            existing_dress_type = DressType.objects.filter(dress_type=dress_type_name).first()
            if existing_dress_type:
                return JsonResponse({'message': 'DressType with the same name already exists'}, status=400)

            # Continue with saving the new DressType to the database
            dress_type = DressType(dress_type=dress_type_name, image=image)
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

def list_product(request):
    return render(request, 'product_grid.html')
