from django.db import models


class Tabacco(models.Model):

    TobaccoId = models.IntegerField(auto_created=True, primary_key=True)
    Mark = models.CharField(max_length=32, default='любой')
    Taste = models.CharField(max_length=32)
    Icon = models.CharField(max_length=32, default='fa fa-leaf')
    Mass = models.IntegerField(default=0)
    Have = models.BooleanField(default=False)

    def __str__(self):
        return f'Taste: {self.Taste} {"Mark: " + self.Mark if self.Mark else ""} {"Mass: " + str(self.Mass) if self.Mass else ""}'


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
        tobaccos = self.TabaccoList.all()
        a = 0
        for t in tobaccos:
            a += 1 if t.Have else 0
        if a:
            return a / len(tobaccos)
        else:
            return -len(tobaccos)

    def __str__(self):
        tobaccos = self.TabaccoList.all()
        return '\n'.join([str(e) for e in tobaccos])
