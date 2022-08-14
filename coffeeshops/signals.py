
from django.core.mail import send_mail 
from django.db.models.signals import post_save, pre_save,post_delete
from django.dispatch import receiver 
from utils import create_slug

from .models import CafeOwner,CoffeeShop,CoffeeShopAddress,Drink


@receiver(post_save, sender = CafeOwner)
def send_new_owner_email(sender,instance,created,**kwargs):
    if created:
        send_mail(
            subject='New Cafe Owner',
            message = f'A new cafe owner has joined named {instance.first_name}{instance.last_name}',
            from_email= "sender@test.com" ,
            recipient_list= ["receiver@test.com"],
            fail_silently=False,
)
        


@receiver(pre_save, sender=CoffeeShop )
def slugify_coffee_shop(sender,instance,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance=instance,slugify_field="name")




@receiver (post_save, sender =CoffeeShop)
def add_default_address(sender,instance,created,**kwargs):
    if created and not instance.location:
        new_location =CoffeeShopAddress.objects.create()
        instance.location = new_location
        instance.save()



@receiver(post_delete, sender =CoffeeShopAddress)
def restore_default_address(sender,instance,**kwargs):
    coffee_shop = instance.coffe_shop
    new_location = CoffeeShopAddress.objects.create(coffee_shop=instance)
    coffee_shop.location = new_location
    coffee_shop.save()


@receiver(pre_save,sender = Drink)
def slugify_coffee_shop(sender,instance,**kwargs):
    if instance.stock_count>0:
        instance.stock_count = False
    else:
        instance.stock_count = True





