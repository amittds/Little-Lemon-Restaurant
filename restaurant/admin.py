from django.contrib import admin
from restaurant.models import Menu, Booking, Customer, Order, OrderItem

admin.site.site_header = "Little Lemon Administration"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"


# Customizing the Menu admin interface
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'status')
    search_fields = ('name',)
    list_filter = ('category', 'status')


# Customizing the Booking admin interface
def mark_as_used(modeladmin, request, queryset):
    queryset.update(is_used=True)


mark_as_used.short_description = "Mark selected bookings as used"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone_number', 'guest_number', 'booking_date', 'booking_time', 'is_used'
    )
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('is_used', 'booking_date')
    ordering = ('booking_date', 'booking_time')
    actions = [mark_as_used]
    date_hierarchy = 'booking_date'


# Customizing the Customer admin interface
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number')
    search_fields = ('full_name', 'mobile_number')


# Customizing the Order admin interface
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'total_price', 'is_confirmed', 'token_number')
    search_fields = ('customer__full_name', 'token_number')
    list_filter = ('is_confirmed', 'created_at')
    ordering = ('-created_at',)


# Customizing the OrderItem inline display in OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_price',)
    extra = 0


# Registering OrderItem with inline display in OrderAdmin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'item_price')
    search_fields = ('menu_item__name',)
    list_filter = ('order__created_at',)


# Adding OrderItem inline to OrderAdmin
OrderAdmin.inlines = [OrderItemInline]
