from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(),
    )
    class Meta:
        # ordering = ['name']
        # indexes = [ models.Index(fields= ['name']) ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse("shop:list_item", args=[self.slug])
    def __str__(self):
        return self.name
class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(),
        description = models.TextField(blank=True),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'products')
    
    #Crud
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_products', null=True, blank=True)
    
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)   
    
    class Meta:
        ordering = ['-created']
        indexes = [
            # models.Index(fields = ['id', 'slug']),
            # models.Index(fields = ['name']),
            models.Index(fields = ['-created']),
        ]
    
    
    def get_absolute_url(self):
        return reverse('shop:detail', args=[ self.id, self.slug])
    def __str__(self):
        return self.name

            
class SellerProfile(models.Model):
    # This links the profile to a single specific Django auth User row
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="seller_profile"
    )
    
    # The flag to differentiate a Seller from a normal Buyer
    is_seller = models.BooleanField(default=False)
    
    # Extra useful e-commerce fields you can utilize later
    store_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Seller: {self.is_seller}"


# =======================================================
# AUTOMATIC PROFILE CREATION (Django Signals)
# =======================================================
# This block guarantees that whenever a User account is created 
# (via django admin, auth views, or standard terminal createsuperuser),
# a corresponding SellerProfile is automatically attached to them.

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # This ONLY runs when a brand new user registers
        SellerProfile.objects.create(user=instance)
    else:
        # For old users who don't have a profile yet, we safely check first
        if not hasattr(instance, 'seller_profile'):
            SellerProfile.objects.create(user=instance)
        else:
            instance.seller_profile.save()