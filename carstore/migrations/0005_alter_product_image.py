# Generated by Django 5.1.3 on 2024-12-09 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carstore', '0004_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
