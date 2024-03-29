# Generated by Django 4.2.10 on 2024-02-28 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ISISUsers', '0004_alter_facility_country_alter_facility_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ISISUsers.facility')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
