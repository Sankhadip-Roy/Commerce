# Generated by Django 4.2.2 on 2023-07-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comments_commentator_comments_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]