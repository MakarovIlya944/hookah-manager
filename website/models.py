from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class Taste(models.Model):

    Taste = models.CharField(max_length=32)
    def __str__(self):
        return self.Taste

class Tabacco(models.Model):

    Brand = models.CharField(max_length=32, default='any')
    Name = models.CharField(max_length=32)
    Icon = models.CharField(max_length=32, default='fa fa-leaf')
    Mass = models.IntegerField(default=0)
    Strength = models.IntegerField(default=5)
    Tastes = models.ManyToManyField(Taste, related_name="Tastes")

    def short(self):
        return "self.Taste" + ((": " + self.Brand) if self.Brand and str(self.Brand) != "any" else "")

    def toJson(self):
        return {
            'have':self.Have, 
            'mass':self.Mass,
            'taste':"self.Taste", 
            'Brand':self.Brand,
            }

    def __str__(self):
        return f'Taste: self.Taste {"Brand: " + self.Brand if self.Brand and str(self.Brand) != "any" else ""} {"Mass: " + str(self.Mass) if self.Mass else ""}'

class Recipe(models.Model):

    LIQUIDS = (
        ('MILK', 'milk'),
        ('WATER', 'water'),
        ('GREEN TEA', 'green tea'),
        ('ICE', 'ice'),
        ('VINE', 'vine'),
    )

    TabaccoList = models.ManyToManyField(Tabacco, related_name="TabaccoList")
    OptionalList = models.ManyToManyField(
        Tabacco, blank=True, related_name="OptionalList")
    Flask = models.CharField(max_length=32, choices=LIQUIDS)
    Description = models.TextField(max_length=128)

    def price(self):
        tabaccos = Tabacco.objects.filter(Have=True).all()
        recipe = self.TabaccoList.all()
        a = 0
        for t in recipe:
            if (t.Brand == 'any' and len(tabaccos.filter(Taste=t.Taste)) > 0) or len(tabaccos.filter(Brand=t.Brand, Taste=t.Taste)) > 0:
                a += 1
        if a:
            return a / len(recipe)
        else:
            return -len(recipe)

    def toJson(self):
        return {
            'options': [o.toJson() for o in self.OptionalList.all()],
            'tabaccos': [t.toJson() for t in self.TabaccoList.all()],
            'flask': str(self.Flask),
            'desc' : str(self.Description)
        }

    def __str__(self):
        tabaccos = self.TabaccoList.all()
        return '\n'.join([str(e) for e in tabaccos])

class Hooker(AbstractUser):

    Tabaccos = models.ForeignKey(Tabacco, null=True, on_delete = models.CASCADE)
    pass

class Feedback(models.Model):
    
    Author = models.ForeignKey(Hooker, on_delete = models.CASCADE)
    TabaccoBrand = models.OneToOneField(
        Tabacco,null=True, blank=True, related_name="TabaccoBrand", on_delete=models.CASCADE)
    RecipeBrand = models.OneToOneField(
        Recipe,null=True, blank=True, related_name="RecipeBrand", on_delete=models.CASCADE)
    Mark = models.IntegerField(default=50)
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.RecipeBrand:
          return 'RecipeBrand: ' + str(self.RecipeBrand)
        else:
          if self.TabaccoBrand:
            return 'TabaccoBrand: ' + str(self.TabaccoBrand)
          else:
            return 'Empty Feedback'
