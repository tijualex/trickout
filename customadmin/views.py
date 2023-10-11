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
def list_neck_pattern(request):
    neck_patterns = NeckPattern.objects.all()
    return render(request, 'neckpattern_grid.html', {'neck_patterns': neck_patterns})

        
#bottom pattern

def list_bottom_pattern(request):
    bottom_patterns = BottomPattern.objects.all()
    return render(request, 'bottompattern_grid.html', {'bottom_patterns': bottom_patterns})

# top pattern

    
def list_top_pattern(request):
    top_patterns = TopPattern.objects.all()
    return render(request, 'toppattern_grid.html', {'top_patterns': top_patterns})


# sleeves
    
def list_sleeves_pattern(request):
    sleeves_patterns = SleevesPattern.objects.all()
    return render(request, 'sleevespattern_grid.html', {'sleeves_patterns': sleeves_patterns})



# fabric
def fabric_grid(request):
    fabrics = Fabric.objects.all()
    return render(request, 'fabric_grid.html', {'fabrics': fabrics})


# dress type

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
    # Fetch users with the role 'user' using UserRole model
    users_with_role_user = UserRole.objects.filter(role='user').select_related('user').values('user')

    # Fetch users where their IDs are in the list of users with the 'user' role
    users = User.objects.filter(id__in=users_with_role_user)

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
    orders = Order.objects.all().order_by('-order_date')
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



from django.shortcuts import render
from customadmin.models import UserRole  # Import UserRole model

from django.db.models import Subquery, OuterRef, Count

def list_designers(request):
    designers = UserRole.objects.filter(role='designer').annotate(
        total_orders=Subquery(
            Order.objects.filter(designer_id=OuterRef('user'))
                 .values('designer_id')
                 .annotate(count=Count('designer_id'))
                 .values('count')[:1]
        ),
        completed_orders=Subquery(
            Order.objects.filter(designer_id=OuterRef('user'), order_status__in=['shipped', 'delivered'])
                 .values('designer_id')
                 .annotate(count=Count('designer_id'))
                 .values('count')[:1]
        )
    )
    return render(request, 'designers_list.html', {'designers': designers})




from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from customadmin.models import UserRole  # Import the UserRole model from your app

def create_designer(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')

        # Check if any of the values are null
        if not (name and username and email and password and cpassword):
            messages.error(request, "Please fill in all the fields")
            return redirect('create_designer')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect('create_designer')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken")
                return redirect('create_designer')
            else:
                # Create a new user using Django's User model
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = name
                user.save()

                # Assign 'designer' role to the new user
                UserRole.objects.create(user=user, role='designer')

                subject = 'Your designer account has been created'
                message = 'Your designer account has been created successfully.'
                from_email = settings.EMAIL_HOST_USER  # Your sender email address
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list)

                return redirect('login_view')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('create_designer')
    return render(request, 'create_designer.html')



# views.py

from django.shortcuts import redirect
from django.contrib.auth.models import User

def activate_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('list_users')

def deactivate_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect('list_users')


def activate_designer(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    # Redirect back to the designers list page after activation
    return redirect('list_designers')

def deactivate_designer(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    # Redirect back to the designers list page after deactivation
    return redirect('list_designers')



# views.py

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from user.models import Order



def get_orders_last_7_days(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    orders_last_7_days = Order.objects.filter(order_date__range=[start_date, end_date]) \
                                      .values('order_date__date') \
                                      .annotate(order_count=Count('order_id')) \
                                      .order_by('order_date__date')
    data = {
        'dates': [order['order_date__date'].strftime('%Y-%m-%d') for order in orders_last_7_days],
        'order_counts': [order['order_count'] for order in orders_last_7_days],
    }
    return JsonResponse(data)


def get_order_status_counts(request):
    delivered_count = Order.objects.filter(order_status='delivered').count()
    processing_count = Order.objects.filter(order_status='processing').count()
    shipped_count = Order.objects.filter(order_status='shipped').count()

    data = {
        'delivered': delivered_count,
        'processing': processing_count,
        'shipped': shipped_count,
    }

    return JsonResponse(data)

