from django.db import models
from picklefield.fields import PickledObjectField
# Create your models here.
class website(models.Model):
   url = models.URLField(max_length=10000)
   words = PickledObjectField()



   def __str__(self):
       return self.url
