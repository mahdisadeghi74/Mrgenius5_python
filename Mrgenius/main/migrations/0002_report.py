# Generated by Django 2.2 on 2019-04-05 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('report_status', models.IntegerField(default=0, verbose_name='report Status')),
                ('fk_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Question')),
            ],
        ),
    ]