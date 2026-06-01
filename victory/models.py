from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone   
# Create your models here.


class Images(models.Model):
    image = models.ImageField(upload_to='Images')
    name = models.CharField(max_length=10)

class Menu_f(models.Model):
    image=models.ImageField(upload_to='food')
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=20)
    text=models.CharField(max_length=100)
    
class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    message = models.TextField()

class down(models.Model):
    head = models.CharField(max_length=50,default="Item")
    image = models.ImageField(upload_to='downs')
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    text = models.TextField()

class Our(models.Model):
    image = models.ImageField(upload_to='Our')
    date = models.DateField()
    head = models.CharField(max_length=50)
    span = models.CharField(max_length=100)
    text = models.CharField(max_length=200)

class Blog(models.Model):
    image = models.ImageField(upload_to='Blog' )
    date = models.DateField()
    head = models.CharField(max_length=50) 
    name = models.CharField(max_length=1000)
    span = models.CharField(max_length=1000)

class Book(models.Model):
    day = models.CharField(max_length=10)
    hour = models.CharField()
    name = models.CharField(max_length=30 , default="name")
    phone = models.CharField(max_length=12)
    person = models.CharField(max_length=10)


class Registration(models.Model):
    fname = models.CharField(max_length=10,null=True)
    lname = models.CharField(max_length=10,null=True)
    email = models.EmailField(max_length=50,null=True)
    password=models.CharField(max_length=8,null=True)

class Login(models.Model):
    email = models.EmailField(max_length=50,null=True)
    password=models.CharField(max_length=8,null=True)

# class Food(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.IntegerField()   # ONLY NUMBER (no ₹, no $)

#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     address = models.TextField()
#     total = models.IntegerField()
#     is_paid = models.BooleanField(default=False)
#     payment_id = models.CharField(max_length=100, blank=True, null=True)



# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     food = models.ForeignKey(Food, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.IntegerField()

class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.IntegerField()

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.food.name} x {self.quantity}"


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
