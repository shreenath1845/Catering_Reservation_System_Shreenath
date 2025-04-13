from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.contrib.auth.views import LogoutView
from .models import MenuItem, CartItem, Order,  OrderItem,  Reservation
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'main/base.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            try:
                profile = Profile.objects.get(user=user)
                if profile.role == 'Admin':
                    return redirect('admin_dashboard')
                elif profile.role == 'Customer':
                    return redirect('customer_dashboard')
                else:
                    messages.error(request, "Invalid role.")
                    return redirect('login')
            except Profile.DoesNotExist:
                messages.error(request, "Profile does not exist.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'main/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, role=role)
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "There was an error creating your account.")
            return redirect('register')

    return render(request, 'main/register.html')

@login_required
def admin_dashboard(request):
    return render(request, 'main/admin_dashboard.html')

@login_required
def add_menu_item_view(request):
    if request.method == 'POST':
        MenuItem.objects.create(
            name=request.POST.get('name'),
            image=request.FILES.get('image'),
            price=request.POST.get('price'),
            description=request.POST.get('description')
        )
        return redirect('view_menu_admin')
    return render(request, 'main/add_item.html')

@login_required
def view_menu_admin(request):
    items = MenuItem.objects.all()
    return render(request, 'main/view_menu.html', {'menu_items': items})

@login_required
def customer_dashboard(request):
    return render(request, 'main/customer_dashboard.html')

class CustomLogoutView(LogoutView):
    next_page = 'home'

@login_required
def view_menu(request):
    query = request.GET.get('q')
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    else:
        menu_items = MenuItem.objects.all()
    cart_item_count = CartItem.objects.filter(user=request.user).count()
    return render(request, 'customer/view_menu_customer.html', {'menu_items': menu_items, 'cart_item_count': cart_item_count})

    



def add_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')


        MenuItem.objects.create(
            name=name,
            image=image,
            price=price,
            description=description
        )

        return redirect('admin_dashboard')
    else:
        return redirect('admin_dashboard')


@login_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        if request.FILES.get('image'):
            item.image = request.FILES['image']
        item.save()
        return redirect('view_menu_admin')
    return render(request, 'admin/edit_menu_item.html', {'item': item})


@login_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    return redirect('view_menu_admin')

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{item.name} added to cart!")
    return redirect('view_menu')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, quantity in cart.items():
        item = MenuItem.objects.get(id=item_id)
        subtotal = item.price * quantity
        total += subtotal
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'customer/my_cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def my_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_data = []

    total = 0
    for item in cart_items:
        subtotal = item.quantity * item.item.price
        total += subtotal
        cart_data.append({
            'id': item.id,
            'item': item.item,
            'quantity': item.quantity,
            'subtotal': subtotal,
        })

    return render(request, 'customer/my_cart.html', {
        'cart_items': cart_data,
        'total': total
    })


@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user,
            customer_name=name,
            phone=phone,
            address=address,
            payment_method=payment_method,
        )


        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity
            )


        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return render(request, 'customer/order_success.html', {'order': order})

    return render(request, 'customer/place_order.html', {'cart_items': cart_items})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-placed_at')
    order_data = []

    for order in orders:
        items = order.order_items.all()
        total = sum(item.item.price * item.quantity for item in items)
        order_data.append({
            'order': order,
            'items': items,
            'total': total
        })

    return render(request, 'customer/my_orders.html', {'order_data': order_data})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('my_cart')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == "Pending":

        order.order_items.all().delete()


        order.delete()

        messages.success(request, "Your order has been cancelled and removed successfully.")
    else:
        messages.warning(request, "Only pending orders can be cancelled and deleted.")

    return redirect('my_orders')

@login_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-placed_at')
    return render(request, 'main/admin_orders.html', {'orders': orders})



@require_POST
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')

    if new_status in dict(Order.STATUS_CHOICES).keys():
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {new_status}.")
    else:
        messages.error(request, "Invalid status selected.")

    return redirect('admin_orders')

@login_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-placed_at')
    return render(request, 'main/admin_orders.html', {'orders': orders})

@login_required
def delete_cancelled_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == 'Cancelled':
        order.delete()
        messages.success(request, f"Cancelled order #{order_id} deleted successfully.")
    else:
        messages.error(request, "Only cancelled orders can be deleted.")

    return redirect('admin_orders')



@login_required
def make_reservation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        number_of_guests = request.POST.get('number_of_guests')
        location = request.POST.get('location')
        additional_notes = request.POST.get('additional_notes')
        food_items = request.POST.getlist('food_items')
        food_items_str = ", ".join(food_items)

        reservation = Reservation.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            email=email,
            event_type=event_type,
            event_date=event_date,
            event_time=event_time,
            number_of_guests=number_of_guests,
            location=location,
            additional_notes=additional_notes,
            food_items=food_items_str,
        )

        messages.success(request, "Reservation booked successfully!")
        return redirect('my_reservations')

    return render(request, 'customer/make_reservation.html')




@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'customer/my_reservations.html', {'reservations': reservations})



@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if reservation.status != 'Cancelled':
        reservation.status = 'Cancelled'
        reservation.save()
        messages.success(request, "Your reservation has been cancelled.")
    return redirect('my_reservations')

@login_required
def admin_reservations(request):
    reservations = Reservation.objects.all().order_by('-event_date')
    return render(request, 'main/admin_reservations.html', {'reservations': reservations})

@require_POST
@login_required
def update_reservation_status(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    new_status = request.POST.get('status')

    if new_status in dict(Reservation.STATUS_CHOICES).keys():
        reservation.status = new_status
        reservation.save()
        messages.success(request, f"Reservation #{reservation_id} updated to {new_status}.")
    else:
        messages.error(request, "Invalid status selected.")

    return redirect('admin_reservations')


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    messages.success(request, f"Reservation #{reservation_id} deleted successfully.")
    return redirect('admin_reservations')

from django.contrib.auth import update_session_auth_hash

@login_required
def customer_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email')
        new_password = request.POST.get('password')

        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()

        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.dob = request.POST.get('dob')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        from django.contrib import messages
        messages.success(request, "✅ Profile updated successfully!")
        return redirect('customer_profile')

    return render(request, 'customer/customer_profile.html', {'profile': profile})
