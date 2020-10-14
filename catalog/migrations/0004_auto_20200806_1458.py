# Generated by Django 3.0.8 on 2020-08-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200806_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='lenguaje',
            field=models.CharField(blank=True, choices=[('E', 'Español'), ('I', 'Íngles')], default='E', help_text='Lenguaje en que esta escrito el libro', max_length=1),
        ),
    ]