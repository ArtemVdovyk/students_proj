# Generated by Django 2.2.25 on 2022-01-11 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20220111_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='students.Group', verbose_name='Група'),
        ),
    ]
