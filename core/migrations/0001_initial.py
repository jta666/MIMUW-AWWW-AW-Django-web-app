# Generated by Django 4.2.1 on 2023-05-09 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('availability_changed_at', models.DateTimeField(auto_now=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_directory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.directory')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('availability_changed_at', models.DateTimeField(auto_now=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('compiled_content', models.TextField(blank=True)),
                ('directory', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.directory')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompilationOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard', models.CharField(choices=[('C89', 'C89'), ('C99', 'C99'), ('C11', 'C11')], default='C89', max_length=10)),
                ('optimization', models.CharField(choices=[('nogcse', 'nogcse'), ('noinvariant', 'noinvariant'), ('noinduction', 'noinduction')], default='nogcse', max_length=12)),
                ('processor', models.CharField(choices=[('MCS51', 'MCS51'), ('Z80', 'Z80'), ('STM8', 'STM8')], default='MCS51', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]