# Generated by Django 2.2.20 on 2021-04-20 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20210420_1219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_activo',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_administrador',
            new_name='is_staff',
        ),
    ]
