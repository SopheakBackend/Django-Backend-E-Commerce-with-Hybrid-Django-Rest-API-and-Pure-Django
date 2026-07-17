from django.contrib import admin
from .models import Category, Product, SellerProfile
from parler.admin import TranslatableAdmin
# Register your models here.
class CategoryAdmin(TranslatableAdmin):
    list_display = [
        'name',
        'slug',
    ]
    def get_prepopulated_fields(self, request, obj = None):
        return {'slug': ('name', )}
admin.site.register(Category, CategoryAdmin)
class ProductAdmin(TranslatableAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated'
    ]

    list_filter = [
        'available',
        'created',
        'updated'
    ]
    list_editable = [
        'price',
        'available'
    ]
    def get_prepopulated_fields(self, request, obj = None):
        return {'slug': ('name', )}
admin.site.register(Product, ProductAdmin)

class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_seller', 'store_name', 'created_at')
    list_filter = ('is_seller', 'created_at')
    search_fields = ('user__username', 'store_name')
    
    # 4. Make fields look clean and organized when editing an individual profile record
    fields = ('user', 'is_seller', 'store_name')
    readonly_fields = ('user',) # Keeps the base user assignment locked to prevent mistakes

    # Custom helper methods to pull linked User details into the display table
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email Address'
admin.site.register(SellerProfile, SellerProfileAdmin)
