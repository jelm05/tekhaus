# Generated by Django 2.2.7 on 2020-06-04 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0019_equipment_reservation_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='reservation_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkouts.Reservation'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Reservation Notes'),
        ),
    ]
