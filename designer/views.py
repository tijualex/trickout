from django.http import JsonResponse
from django.shortcuts import render
from customadmin.models import Designs
from django.contrib.auth.models import User

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
def order_list(request):
    orders = Order.objects.all()

    # Filtering logic
    status_filter = request.GET.get('status', None)
    if status_filter in ['processing', 'shipped', 'delivered']:
        orders = orders.filter(order_status=status_filter)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'order_date')
    orders = orders.order_by(sort_by)

    return render(request, 'designer_dash/order_list.html', {'orders': orders})


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
    design = get_object_or_404(Designs, design_id=design_id)
    measurements = PersonMeasurement.objects.filter(design=design)

    return render(request, 'designer_dash/design_details.html', {'design': design, 'measurements': measurements})


def measurement_details(request, measurement_id):
    measurement = get_object_or_404(PersonMeasurement, measurement_id=measurement_id)
    return render(request, 'measurement_details.html', {'measurement': measurement})