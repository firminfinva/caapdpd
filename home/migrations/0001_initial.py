# Generated by Django 5.0.3 on 2024-03-12 20:23

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='Votre nom', max_length=20, unique=True)),
                ('phone', models.CharField(default='+243', max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Le numéro de téléphone doit être saisi au format : '+243...'.jusqu'à 14 chiffres autorisés", regex='^(\\+\\d{1,3})?,?\\s?\\d{9,13}$')])),
                ('email', models.EmailField(default='@gmail.com', max_length=254)),
                ('ville', models.CharField(choices=[('Bukavu', 'Bukavu'), ('Butembo', 'Butembo'), ('Goma', 'Goma'), ('Kinshasa', 'Kinshasa'), ('Lubumbashi', 'Lubumbashi')], default='Goma', max_length=100)),
                ('sexe', models.CharField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme', max_length=20)),
                ('age', models.DateField(blank=True, default='2002-01-14', null=True)),
                ('image', models.ImageField(blank=True, default='placeholder.png', null=True, upload_to='')),
                ('active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timeatamp', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_key', models.CharField(blank=True, max_length=32, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('forget_password_token', models.CharField(max_length=100)),
                ('lien', models.CharField(default='lien', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
