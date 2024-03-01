from django.contrib.auth.models import User
from django.db import models


class CategoryProduct(models.Model):
    icon = models.ImageField(upload_to='icon/')
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

    def products_count(self):
        products = Product.objects.filter(category=self)
        return products.count()


class Product(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to="product/")
    price = models.IntegerField(blank=False, null=False)
    num_of_buy = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_cart_total_price(self):
        items = self.shoppingcartitem_set.all()
        total = sum([item.get_total() for item in items])
        return total

    def get_cart_total_items(self):
        items = self.shoppingcartitem_set.all()
        total = sum([item.quantity for item in items])
        return total


class ShoppingCartItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Vote(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    date_submitted = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title if len(self.title) < 25 else self.title[:20]+"..."}'


class SingleVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    is_agree = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
