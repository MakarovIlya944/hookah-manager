# Generated by Django 2.2.7 on 2020-09-10 16:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hooker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Taste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Taste', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Tabacco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brand', models.CharField(default='any', max_length=32)),
                ('Name', models.CharField(max_length=32)),
                ('Icon', models.CharField(default='fa fa-leaf', max_length=32)),
                ('Mass', models.IntegerField(default=0)),
                ('Strength', models.IntegerField(default=5)),
                ('Tastes', models.ManyToManyField(related_name='Tastes', to='website.Taste')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Flask', models.CharField(choices=[('MILK', 'milk'), ('WATER', 'water'), ('GREEN TEA', 'green tea'), ('ICE', 'ice'), ('VINE', 'vine')], max_length=32)),
                ('Description', models.TextField(max_length=128)),
                ('OptionalList', models.ManyToManyField(blank=True, related_name='OptionalList', to='website.Tabacco')),
                ('TabaccoList', models.ManyToManyField(related_name='TabaccoList', to='website.Tabacco')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mark', models.IntegerField(default=50)),
                ('Date', models.DateField(auto_now_add=True)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('RecipeBrand', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RecipeBrand', to='website.Recipe')),
                ('TabaccoBrand', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TabaccoBrand', to='website.Tabacco')),
            ],
        ),
        migrations.AddField(
            model_name='hooker',
            name='Tabaccos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Tabacco'),
        ),
        migrations.AddField(
            model_name='hooker',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='hooker',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
