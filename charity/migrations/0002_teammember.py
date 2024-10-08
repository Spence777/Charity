# Generated by Django 5.1 on 2024-09-11 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('image', models.ImageField(upload_to='team_images/')),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
