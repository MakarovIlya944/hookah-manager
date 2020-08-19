from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tabacco(models.Model):

    TobaccoId = models.IntegerField(auto_created=True, primary_key=True)
    Mark = models.CharField(max_length=32, default='любой')
    Taste = models.CharField(max_length=32)
    Icon = models.CharField(max_length=32, default='fa fa-leaf')
    Mass = models.IntegerField(default=0)
    Have = models.BooleanField(default=False)

    def __str__(self):
        return f'Taste: {self.Taste} {"Mark: " + self.Mark if self.Mark and str(self.Mark) != "любой" else ""} {"Mass: " + str(self.Mass) if self.Mass else ""}'

class Recipe(models.Model):

    LIQUIDS = (
        ('MILK', 'milk'),
        ('WATER', 'water'),
        ('GREEN TEA', 'green tea'),
        ('ICE', 'ice'),
        ('VINE', 'vine'),
    )

    RecipeId = models.IntegerField(auto_created=True, primary_key=True)
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
            if (t.Mark == 'любой' and len(tabaccos.filter(Taste=t.Taste)) > 0) or len(tabaccos.filter(Mark=t.Mark, Taste=t.Taste)) > 0:
                a += 1
        if a:
            return a / len(recipe)
        else:
            return -len(recipe)

    def __str__(self):
        tabaccos = self.TabaccoList.all()
        return '\n'.join([str(e) for e in tabaccos])

class Feedback(models.Model):
    FeedbackId = models.IntegerField(auto_created=True, primary_key=True)
    TabaccoMark = models.OneToOneField(
        Tabacco, blank=True, related_name="TabaccoMark", on_delete=models.CASCADE)
    RecipeMark = models.OneToOneField(
        Recipe, blank=True, related_name="RecipeMark", on_delete=models.CASCADE)
    Mark = models.IntegerField(default=50)
    
    def __str__(self):
        if self.RecipeMark:
          return 'RecipeMark: ' + str(self.RecipeMark)
        else:
          if self.TabaccoMark:
            return 'TabaccoMark: ' + str(self.TabaccoMark)
          else:
            return 'Empty Feedback'

class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    FeedbackList = models.ManyToManyField(
        Feedback, blank=True, related_name="FeedbackList")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
