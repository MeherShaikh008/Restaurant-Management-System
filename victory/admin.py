from django.contrib import admin
from .models import*

admin.site.register(Images)

class Menu(admin.ModelAdmin):
    list_display=['image','name','price','text']
admin.site.register(Menu_f,Menu)

class OurBlog(admin.ModelAdmin):
    list_display = ['image','date','head','span','text']
admin.site.register(Our,OurBlog)

class BookTable(admin.ModelAdmin):
    list_display = ['day','hour','name','phone','person']
admin.site.register(Book,BookTable)

class Down(admin.ModelAdmin):
    list_display=['head','name','image','price','text']
admin.site.register(down,Down)

class Blog_p(admin.ModelAdmin):
    list_display=['image','date','head','name','span']
admin.site.register(Blog,Blog_p)

class Contact(admin.ModelAdmin):
    list_display=['name','email','phone','message']
admin.site.register(ContactForm,Contact)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('food', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'total_amount')
    readonly_fields = ('total_amount',)
    inlines = [OrderItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'razorpay_order_id', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('razorpay_order_id',)