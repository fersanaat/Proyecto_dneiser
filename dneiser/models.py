from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.
class User(AbstractUser):
    username= models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    country =models.CharField(max_length=100,blank=True, null=True)
    creted_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
          db_table ="users"
          verbose_name = 'Usuario'
          verbose_name_plural= 'Usuarios'
         
    def __str__(self):
          return f"{self.username} ({self.email})"

class Category(models.Model):
     name = models.CharField(
        max_length=100,
        verbose_name="Nombre"
    )
     description = models.TextField(
        null = True,
        verbose_name= "Descripcion"
    )
     class Meta:
        db_table = "categories"
        verbose_name = 'Categoria'
        verbose_name_plural= 'Categorias'
        
     def __str__(self):
        return f"{self.name} - {self.description}"

class Product(models.Model):
    
    
    image = models.ImageField(
    verbose_name='Imagen',
    upload_to='dneiser/categories/',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    blank=True,
    null=True
    
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio"
    )
    
    stock = models.IntegerField(
        default=0,
        verbose_name="Inventario"
    )
    
    description = models.TextField(
        null = True,
        verbose_name= "Descripcion"
    )
    
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "products"
        verbose_name = 'Producto'
        verbose_name_plural= 'Productos'
    
    def __str__(self):
        return f"{self.name} - ${self.price} - {self.description} - {self.stock}"
        
        
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)
        