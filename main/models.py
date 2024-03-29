from django.db import models
from django.contrib.auth.models import AbstractUser
from main.funcs import generate_code


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/',default='avatar/default.png')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'default.png'
        super().save(*args, **kwargs)
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, blank=True,unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.code = generate_code()
        super(Category,self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, 
                                         blank=True, null=True)
    banner_img = models.ImageField(upload_to='banner-img/')
    quantity = models.IntegerField() 
    delivery = models.BooleanField(default=False)
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.code = generate_code()
        super(Product,self).save(*args, **kwargs)



class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/')


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video', blank=True, null=True)
    link = models.URLField(null=True, blank=True)


class Review(models.Model):
    mark = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk:
            obj = Review.objects.filter(product=self.product, user=self.user).exclude(pk=self.pk).first()
        else:
            obj = Review.objects.filter(product=self.product, user=self.user).first()
        
        if obj:
            obj.mark = self.mark
            obj.text = self.text
            obj.save() 
        else:
            super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=255, blank=True,unique=True)
    is_active = models.BooleanField(default=True)

    def save(self,*args, **kwargs):
        if not self.id:
            self.code = generate_code()
        return super(Cart, self).save(*args, **kwargs)

class CartProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    count = models.IntegerField()

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)