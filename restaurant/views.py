from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Menu, Booking, Customer, Order, OrderItem, OPENING_HOUR, CLOSING_HOUR
from django.contrib import messages
from django.db import transaction
from datetime import date, timedelta


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save()
        print(f"Booking ID: {booking.id}")  # Debug line to check booking ID
        messages.success(request, "Booking confirmed!")
        return redirect('booking_confirmation', pk=booking.pk)
    elif request.method == 'POST':
        print("Form errors:", form.errors)  # Debug line for form errors
        messages.error(request, "Please correct the errors below.")

    return render(request, 'book.html', {'form': form})


def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_confirmation.html', {'booking': booking})


def review_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'review_booking.html', {'booking': booking})


def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking canceled successfully.")
        return redirect('booking_canceled')
    return render(request, 'cancel_booking.html', {'booking': booking})


def booking_canceled(request):
    return render(request, 'booking_canceled.html')


def menu(request):
    categories = Menu.objects.values_list('category', flat=True).distinct()
    menu_by_category = {category: Menu.objects.filter(category=category) for category in categories}

    context = {'menu_by_category': menu_by_category}
    return render(request, "menu.html", context)


def category_menu(request, category_name):
    menu_items = Menu.objects.filter(category=category_name)
    if not menu_items:
        messages.info(request, "No items found in this category.")

    context = {'menu_items': menu_items, 'category_name': category_name}
    return render(request, "category_menu.html", context)


def display_menu_items(request, pk=None):
    menu_item = get_object_or_404(Menu, pk=pk)
    return render(request, "menu_item.html", {'menu_item': menu_item})


def customer_login(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        full_name = request.POST.get('full_name')

        # Check if customer exists or create a new one
        customer, created = Customer.objects.get_or_create(
            mobile_number=mobile_number,
            defaults={'full_name': full_name}
        )
        request.session['customer_id'] = customer.id
        messages.success(request, "Logged in successfully.")
        return redirect('order_menu')

    return render(request, 'customer_login.html')


def customer_logout(request):
    # Clear the customer's session
    request.session.flush()  # This clears the entire session
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to the home page or any desired page


def order_menu(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')  # Redirect if no customer is logged in

    categories = Menu.objects.values_list('category', flat=True).distinct()
    menu_by_category = {category: Menu.objects.filter(category=category, status=1) for category in categories}

    return render(request, 'menu.html', {'menu_by_category': menu_by_category})


@transaction.atomic
def add_to_cart(request, menu_id):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return JsonResponse({'success': False, 'message': "You need to log in."})

    menu_item = get_object_or_404(Menu, id=menu_id)
    customer = Customer.objects.get(id=customer_id)

    # Create or get an open order
    order, created = Order.objects.get_or_create(customer=customer, is_confirmed=False)

    # Add or update an item in the order
    order_item, item_created = OrderItem.objects.get_or_create(order=order, menu_item=menu_item)
    if not item_created:
        order_item.quantity += 1  # Increase quantity if item already exists
    order_item.save()

    return JsonResponse({'success': True, 'message': f"Added {menu_item.name} to your cart."})


def confirm_order(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer does not exist.")
        return redirect('customer_login')

    customer = Customer.objects.get(id=customer_id)
    order = get_object_or_404(Order, customer=customer, is_confirmed=False)

    if request.method == "POST":
        # Confirm order
        order.is_confirmed = True
        order.save()
        messages.success(request, "Order confirmed! Your token number is " + order.token_number)
        return redirect('order_summary', pk=order.pk)

    return render(request, 'confirm_order.html', {'order': order})


def update_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if 'quantity' in request.POST:
        quantity = int(request.POST['quantity'])
        if quantity > 0:
            order_item.quantity = quantity
            order_item.save()
            messages.success(request, "Quantity updated.")
        else:
            order_item.delete()  # Remove item if quantity is set to 0
            messages.success(request, "Item removed from cart.")

    return redirect('confirm_order')


def order_summary(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_summary.html', {'order': order})
