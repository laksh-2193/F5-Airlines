# Generated by Django 4.0.3 on 2022-05-24 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_userdetails_contactno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('acronym', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('placename', models.CharField(max_length=20)),
                ('lattitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
            ],
        ),
    ]
