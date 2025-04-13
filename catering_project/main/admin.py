from django.contrib import admin
from .models import Profile, MenuItem, CartItem, Order

# Profile admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

# MenuItem admin
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

# CartItem admin
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    list_filter = ('user',)

# Order admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'status', 'payment_method', 'placed_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('customer_name', 'phone', 'address')
    ordering = ('-placed_at',)
    list_editable = ('status',)

# Registering models
admin.site.register(Profile, ProfileAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
