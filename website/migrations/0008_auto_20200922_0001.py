# Generated by Django 2.2.7 on 2020-09-21 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20200921_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='Description',
            field=models.TextField(blank=True, default='', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='Tabaccos',
            field=models.ManyToManyField(blank=True, related_name='RecipeTabaccos', to='website.Tabacco'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='Tastes',
            field=models.ManyToManyField(blank=True, related_name='RecipeTastes', to='website.Taste'),
        ),
    ]