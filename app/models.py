from django.db import models

# Create your models here.
class User_data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    mobile = models.CharField(max_length=16)
    password = models.CharField(max_length=256)
    vr_code = models.CharField(max_length=256,blank=True)
    vr_code_status = models.IntegerField(default=0)
    user_type = models.CharField(max_length=256)
    address = models.TextField(blank=True)
    image = models.CharField(max_length=256,blank=True)
    secondary_address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    active = models.CharField(blank=True,default="Active",max_length=256)

class Admin_user(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    mobile = models.CharField(max_length=16)
    role = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    image = models.CharField(max_length=256,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=256,blank=True)
    address_active = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey(User_data, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='user_address')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    subject = models.CharField(max_length=1048,null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='menu_category')
    name = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    image = models.CharField(max_length=256,null=True)
    description = models.TextField(blank=True)
    delivery_type = models.CharField(max_length=256,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Meals(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='meals_category')
    item = models.CharField(max_length=256)
    fixed_item = models.CharField(max_length=256)
    fixed_item_quantity = models.CharField(max_length=256)
    qty = models.CharField(max_length=256,null=True)
    meal_text = models.CharField(max_length=256,null=True)
    delivery_price = models.CharField(max_length=256,null=True)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=256)
    day = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    specials = models.CharField(max_length=256,null=True)
    delivery_type = models.CharField(max_length=256,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    type = models.CharField(max_length=256,null=True,default="meals")
    combo = models.CharField(max_length=256, null=True)

class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256,null=True)
    image = models.CharField(max_length=256,null=True)
    services = models.CharField(max_length=256, null=True)
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Code(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=16)
    food_available = models.CharField(max_length=256)
    service = models.CharField(max_length=256,default="Regular Timing")
    delivery_type = models.CharField(max_length=256)
    delivery_EST = models.CharField(max_length=256)
    amount = models.CharField(max_length=256,null=True)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='code_driver')
    timefrom = models.TimeField(default='00:00:00')
    timeto = models.TimeField(default='00:00:00')
    delfrom = models.TimeField(default='00:00:00')
    delto = models.TimeField(default='00:00:00')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)


class Size(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Variations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Promocodes(models.Model):
    id = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=256)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.CharField(max_length=256)
    min_amt = models.CharField(max_length=256)
    discount = models.CharField(max_length=256)
    discount_type = models.CharField(max_length=256,null=True)
    amount = models.CharField(max_length=256, null=True)
    customer = models.ForeignKey(User_data, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='promo_user')
    services = models.CharField(max_length=256,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Timings(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=256)
    open_time = models.TimeField()
    close_time = models.TimeField()
    delivery = models.CharField(max_length=256,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Takeawayclosetime(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=256)
    items = models.TextField(blank=True)
    order_date = models.CharField(max_length=256)
    user_date = models.ForeignKey(User_data, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='order_user')
    meals_date = models.ForeignKey(Meals, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='order_meals')

    order_status = models.CharField(max_length=256)
    order_type = models.CharField(max_length=256,null=True)

    order_price = models.FloatField(default=0, null=True)
    order_qty = models.IntegerField(default=0, null=True)
    order_delivery_price = models.FloatField(null=True,default=0)
    order_discount_price = models.FloatField(null=True,default=0)

    combo_type = models.CharField(max_length=256, null=True)
    bal_combo = models.CharField(max_length=256, null=True)
    order_address = models.CharField(max_length=256, null=True)
    order_address_customer = models.ForeignKey(Code, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='order_code')
    total_amt = models.CharField(max_length=256, null=True)
    single_item = models.CharField(max_length=256, null=True)
    payment_status = models.CharField(max_length=256, null=True,default="Not Paid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_date_time = models.CharField(max_length=256,null=True)

    status = models.IntegerField(default=0)

class Subscriber_list(models.Model):
    id = models.AutoField(primary_key=True)
    user_data = models.ForeignKey(User_data, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='subscriber_user')
    code = models.CharField(max_length=256, null=True)
    meal_type = models.CharField(max_length=256, null=True)
    sub_status = models.CharField(max_length=256, null=True)
    sub_order_ids = models.CharField(max_length=256, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Balance(models.Model):
    id = models.AutoField(primary_key=True)
    user_data = models.ForeignKey(User_data, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='balance_user')
    date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=256, null=True)
    note = models.CharField(max_length=256, null=True)
    transition_type = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    user_data = models.ForeignKey(User_data, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='note_user')
    note = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Catering_menu(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)