from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
# CarList is a database here stored in SQLite database
def alphanumeric(value):
    if not str(value).isalnum():
        raise ValidationError("value must be alphanumeric")
    return value

class ShowRoomList(models.Model):
    name=models.CharField(max_length=30)
    location=models.CharField(max_length=100)
    website=models.URLField(max_length=100)
    
    def __str__(self):
        return self.name


class CarList(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=20)
    active=models.BooleanField(default=False)
    carnumber=models.CharField(max_length=29,blank=True,null=True,validators=[alphanumeric])
    price=models.DecimalField(max_digits=9,decimal_places=2,blank=True,null=True)
    showroom=models.ForeignKey(ShowRoomList,on_delete=models.CASCADE,null=True,related_name='showrooms')

    def __str__(self):
        return self.name
    
class Review(models.Model):
    apiuser=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    rating=models.IntegerField(validators=[MaxValueValidator,MinValueValidator])
    comments=models.CharField(max_length=20)
    car=models.ForeignKey(CarList, on_delete=models.CASCADE,null=True,related_name='Reviews')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.car.name+" rating is "+" "+ str(self.rating)
    