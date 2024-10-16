# Generated by Django 5.1.1 on 2024-10-16 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=400)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CheckedTender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.IntegerField(unique=True)),
                ('category_id', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Checked tenders',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Telegram users',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=400)),
                ('product_code', models.CharField(blank=True, max_length=400, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etenderuzex.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=400)),
                ('display_number', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('1', 'Tender'), ('2', 'Auction')], max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('clarific_date', models.DateTimeField(blank=True, null=True)),
                ('cost', models.FloatField()),
                ('currency', models.CharField(choices=[('106', 'UZS'), ('14', 'USD'), ('15', 'EUR'), ('20', 'RUB')], max_length=50)),
                ('seller_name', models.CharField(blank=True, max_length=100, null=True)),
                ('seller_tin', models.CharField(blank=True, max_length=50, null=True)),
                ('region_name', models.CharField(blank=True, max_length=100, null=True)),
                ('district_name', models.CharField(blank=True, max_length=100, null=True)),
                ('seller_id', models.IntegerField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='etenderuzex.category')),
            ],
            options={
                'verbose_name_plural': 'Tenders',
            },
        ),
        migrations.CreateModel(
            name='TenderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='etenderuzex.product')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etenderuzex.tender')),
            ],
            options={
                'verbose_name_plural': 'Tender products',
            },
        ),
    ]
