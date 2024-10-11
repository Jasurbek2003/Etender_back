from django.db import models


class Category(models.Model):
    category_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'


def type_choices():
    return (
        ('1', 'Tender'),
        ('2', 'Auction'),
    )


def currency_choices():
    return (
        ('106', 'UZS'),
        ('14', 'USD'),
        ('15', 'EUR'),
        ('20', 'RUB'),
    )


class Tender(models.Model):
    tender_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=400)
    display_number = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=type_choices())
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    clarific_date = models.DateTimeField(null=True, blank=True)
    cost = models.FloatField()
    currency = models.CharField(max_length=50, choices=currency_choices())
    seller_name = models.CharField(max_length=100, blank=True, null=True)
    seller_tin = models.CharField(max_length=50, blank=True, null=True)
    region_name = models.CharField(max_length=100, blank=True, null=True)
    district_name = models.CharField(max_length=100, blank=True, null=True)
    seller_id = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tenders'


class TenderProduct(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.tender} - {self.product}"

    class Meta:
        verbose_name_plural = 'Tender products'


class CheckedTender(models.Model):
    tender_id = models.IntegerField(unique=True)
    category_id = models.IntegerField()

    def __str__(self):
        return f"{self.tender_id} - {self.category_id}"

    class Meta:
        verbose_name_plural = 'Checked tenders'


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_id}-{self.username}"

    class Meta:
        verbose_name_plural = 'Telegram users'
