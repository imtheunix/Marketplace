from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField, SlugField
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(max_length=320)
    profilepic = models.ImageField(null=True, blank=True)
    backgroundpic = models.ImageField(null=True)
    descricao_user = models.TextField(max_length=250, null=True, blank=True)
    comentario = models.TextField(max_length=500, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    pass


class Robos(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=150)
    reviews = models.IntegerField(null=True, blank=True)
    robocode = models.FileField(null=True, blank=True, upload_to="codigo")
    robopic = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/imagens",
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preco = models.DecimalField(decimal_places=8, max_digits=20, null=True, blank=True)
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(default=slugify(nome), unique=True)

    def clean(self):
        if self.preco == None:
            raise ValidationError(_("Válido apenas numero positivo maior que 0.00000001"))
        elif self.preco < 0.00000001:
            raise ValidationError(_("Válido apenas numero positivo maior que 0.00000001"))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super(Robos, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

    def get_add_to_cart_url(self):
        return reverse("leads:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("leads:remove-from-cart", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, blank=True, null=True
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Robos, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    status = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantidade} of {self.item.nome}"

    def get_total_item_price(self):
        return self.quantidade * self.item.preco

    def get_total_discount_item_price(self):
        return self.quantidade * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Carrinho(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey(
        "Address",
        related_name="shipping_address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_address = models.ForeignKey(
        "Address",
        related_name="billing_address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"
