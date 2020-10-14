# Generated by Django 3.0.8 on 2020-09-23 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0004_auto_20200806_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancialibro',
            name='prestamo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='libro',
            name='lenguaje',
            field=models.CharField(blank=True, choices=[('E', 'Español'), ('I', 'Inglés')], default='E', help_text='Lenguaje en que esta escrito el libro', max_length=1),
        ),
    ]
