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

class Hooker(AbstractUser):
    pass

class Tabacco(models.Model):

    Brand = models.CharField(max_length=32, default='')
    Name = models.CharField(max_length=32)
    Keepers = models.ManyToManyField(Hooker, blank=True, related_name="Keepers")
    Icon = models.CharField(max_length=32, default='fa fa-leaf')
    Mass = models.IntegerField(default=0)
    Strength = models.IntegerField(default=5)
    Tastes = models.ManyToManyField(Taste, related_name="Tastes")

    def short(self):
        return self.Brand + ": " + self.Name

    def toJson(self):
        tastes = self.Tastes.all()
        tastes = [str(t) for t in tastes]
        return {
            'mass':self.Mass,
            'taste':'['+{",".join(tastes)}+']', 
            'brand':self.Brand,
            'name':self.Name,
            'strength':self.Strength,
            }

    def __str__(self):
        tastes = self.Tastes.all()
        tastes = [str(t) for t in tastes]
        return f'{"Brand: " + self.Brand + " " if self.Brand and str(self.Brand) != "any" else ""}Name: {self.Name} [{",".join(tastes)}]{" Mass: " + str(self.Mass) if self.Mass else ""}'

class Recipe(models.Model):

    LIQUIDS = (
        ('WATER', 'water'),
        ('MILK', 'milk'),
        ('GREEN TEA', 'green tea'),
        ('ICE', 'ice'),
        ('VINE', 'vine'),
    )

    Tabaccos = models.ManyToManyField(Tabacco, blank=True, related_name="RecipeTabaccos")
    Tastes = models.ManyToManyField(Taste, blank=True, related_name="RecipeTastes")
    Flask = models.CharField(max_length=32, choices=LIQUIDS)
    Description = models.TextField(max_length=128, default="")

    def price(self, username):
        tabaccos = Tabacco.objects.filter(Keepers__username=username)
        a = 0
        if self.Tabaccos:
            recipe = self.Tabaccos.all()
            for t in recipe:
                if len(tabaccos.filter(Brand=t.Brand, Taste=t.Taste)) > 0:
                    a += 1
        else:
            recipe = self.Tastes.all()
            for t in recipe:
                if len(tabaccos.filter(Tastes__contain=t.Taste)) > 0:
                    a += 1
        if a:
            return a / len(recipe)
        else:
            return -len(recipe)

    def toJson(self):
      res = {
        'flask': str(self.Flask),
        'desc' : str(self.Description)
      }
      if self.Tabaccos:
        res['tabaccos'] = [t.toJson() for t in self.Tabaccos.all()]
      else:
        res['tastes'] = [str(t) for t in self.Tastes.all()]
      return res

    def __str__(self):
      if len(self.Tabaccos) > 0:
        tabaccos = self.Tabaccos.all()
        return '\n'.join([str(e) for e in tabaccos])
      else:
        tastes = self.Tastes.all()
        return '['+','.join([str(e) for e in tastes])+']'

class Feedback(models.Model):
    
    Author = models.ForeignKey(Hooker, on_delete = models.CASCADE)
    TabaccoList = models.OneToOneField(
        Tabacco,null=True, blank=True, related_name="TabaccoList", on_delete=models.CASCADE)
    RecipeList = models.OneToOneField(
        Recipe,null=True, blank=True, related_name="RecipeList", on_delete=models.CASCADE)
    Mark = models.IntegerField(default=50)
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.RecipeList:
          return 'RecipeList: ' + str(self.RecipeList)
        else:
          if self.TabaccoList:
            return 'TabaccoList: ' + str(self.TabaccoList)
          else:
            return 'Empty Feedback'
