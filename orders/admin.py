from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.urls import reverse
import csv
import datetime
from django.http import HttpResponse
# Register your models here.

#function used to trigger the pdf function in view.py
def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args = [obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


#function used to display one specific order object in admin site
def order_detail(obj):
    url = reverse('orders:admin_order_detail', args = [obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

#custom action in admin page and convert into CSV file
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = (
        f'attachment; filename={opts.verbose_name}.csv'
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field 
        #get all fields in opts, which refer to Order model
        for field in opts.get_fields()
        #get all fields except many to many and one to many
        if not field.many_to_many and not field.one_to_many
    ]
    
    writer.writerow([field.verbose_name for field in fields])
    
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'
                


#function for creating dynamic stripe link and display it 
def order_payment(obj):
    url = obj.get_stripe_id()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Stripe payment'
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        order_payment,
        'created',
        'updated',
        order_detail,
        order_pdf,
    ]
    list_filter = [
        'paid',
        'created',
        'updated',
    ]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
admin.site.register(Order, OrderAdmin)