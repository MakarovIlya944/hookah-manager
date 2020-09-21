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

class Icon(models.Model):
  DEFAULT = 'DEFAULT'
  ROCKET = 'ROCKET'
  ANIMAL = 'ANIMAL'
  ELEMENT = 'ELEMENT'
  SUPPORT = 'SUPPORT'
  
  ICONS = (
    (DEFAULT, 'fa fa-leaf'),
    (ROCKET, 'fas fa-space-shuttle'),
    (ANIMAL, 'fas fa-paw'),
    (ELEMENT, 'fab fa-elementor'),
    (SUPPORT, 'icon-support'),
  )

  Icon = models.CharField(max_length=32, choices=ICONS, default=DEFAULT, primary_key=True)

  def choose_icon(brand):
    if brand == 'darkside':
      return Icon.ROCKET
    elif brand == 'sebero':
      return Icon.ANIMAL
    elif brand == 'element':
      return Icon.ELEMENT
    elif brand == 'dailyhookah':
      return Icon.SUPPORT
    else:
      return Icon.DEFAULT
  
  def icon(self):
    t = self.ICONS[0][1]
    for i in self.ICONS:
      if self.Icon == i[0]:
        t = i[1]
        break
    return t

  def __str__(self):
    return self.Icon + ": " + self.icon()

class Tabacco(models.Model):

  Brand = models.CharField(max_length=32, default='')
  Name = models.CharField(max_length=32)
  Keepers = models.ManyToManyField(Hooker, blank=True, related_name="Keepers")
  Icon = models.ForeignKey(Icon, null=True, blank=True, related_name="TabaccoIcon", on_delete = models.SET_NULL)
  Mass = models.IntegerField(default=0)
  Tastes = models.ManyToManyField(Taste, related_name="TabaccoTastes")
  Strength = models.IntegerField(default=5)

  def short(self):
    return self.Brand + ": " + self.Name
  short.admin_order_field = 'brand_name'
  brand_name = property(short)

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
    tastes = [str(t) for t in self.Tastes.all()]
    return f'{self.Brand}: {self.Name} [{",".join(tastes)}]{" Mass: " + str(self.Mass) if self.Mass else ""}'

class Recipe(models.Model):
    WATER = 'WATER'
    MILK = 'MILK'
    GREENTEA = 'GREENTEA'
    ICE = 'ICE'
    VINE = 'VINE'
    LIQUIDS = (
        (WATER, 'water'),
        (MILK, 'milk'),
        (GREENTEA, 'green tea'),
        (ICE, 'ice'),
        (VINE, 'vine'),
    )

    Tabaccos = models.ManyToManyField(Tabacco, blank=True, related_name="RecipeTabaccos")
    Tastes = models.ManyToManyField(Taste, blank=True, related_name="RecipeTastes")
    Flask = models.CharField(max_length=32, choices=LIQUIDS, default=WATER)
    Description = models.TextField(max_length=128, default="")

    def price(self, username):
        tabaccos = Tabacco.objects.filter(Keepers__username=username)
        a = 0
        if self.Tabaccos:
            recipe = self.Tabaccos.all()
            for t in recipe:
                if len(tabaccos.filter(Brand=t.Brand, Name=t.Name)) > 0:
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
      if len(self.Tabaccos.all()) > 0:
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
