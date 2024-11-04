from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from datetime import date, time, timedelta
import uuid

# Constants
OPENING_HOUR = time(14, 0)  # Example: 2 PM
CLOSING_HOUR = time(22, 0)  # Example: 10 PM

CATEGORY_CHOICES = [
    ('Brunch', 'brunch'),
    ('Appetizer', 'appetizer'),
    ('Sides', 'sides'),
    ('Entrees', 'entrees'),
    ('Specials', 'specials'),
    ('Vegan', 'vegan'),
    ("Beverages", "beverages"),
    ("Desserts", "desserts"),
]

STATUS_CHOICES = [
    (0, 'Unavailable'),
    (1, 'Available'),
]


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message="Enter a 10-digit mobile number.")]
    )

    def __str__(self):
        return f"{self.full_name} ({self.mobile_number})"


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(regex=r'^\d{10}$',
                                   message="Phone number must be a valid number. E.g., '9876543210' ")],
    )
    guest_number = models.PositiveIntegerField()
    booking_date = models.DateField(default=date.today)
    booking_time = models.TimeField(default=OPENING_HOUR)
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def clean(self):
        if not (date.today() <= self.booking_date <= (date.today() + timedelta(days=7))):
            raise ValidationError("Booking date must be within the next 7 days.")
        if not (OPENING_HOUR <= self.booking_time <= CLOSING_HOUR):
            raise ValidationError(
                f"Booking time must be between {OPENING_HOUR.strftime('%I:%M %p')} and {CLOSING_HOUR.strftime('%I:%M %p')}."
            )

    def get_booking_time_am_pm(self):
        return self.booking_time.strftime('%I:%M %p')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.booking_date} at {self.get_booking_time_am_pm()}"

    class Meta:
        ordering = ['booking_date', 'booking_time']


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(max_length=1000, blank=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='entrees'
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'order', 'name']


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True)
    is_confirmed = models.BooleanField(default=False)
    token_number = models.CharField(max_length=6, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token_number:
            self.token_number = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return sum(item.menu_item.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} - {self.customer.full_name}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.item_price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order {self.order.id}"
