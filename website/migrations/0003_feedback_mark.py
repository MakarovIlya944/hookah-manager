# Generated by Django 2.2.7 on 2020-07-22 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_feedback_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='Mark',
            field=models.IntegerField(default=50),
        ),
    ]