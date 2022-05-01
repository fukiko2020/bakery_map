from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = "custom_user"
    # pass


class Bakery(models.Model):
    name = models.CharField(verbose_name="店名", max_length=30)
    longitude = models.IntegerField(verbose_name="経度")
    latitude = models.IntegerField(verbose_name="緯度")
    place_id = models.CharField(max_length=200)


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, default="user",
        related_name="review_user",
        on_delete=models.SET_DEFAULT
    )
    bakery = models.ForeignKey(
        Bakery,
        default="deleted",
        related_name="review_bakery",
        on_delete=models.SET_DEFAULT
    )
    comment = models.TextField(verbose_name="本文")
    pub_date = models.DateTimeField(verbose_name="投稿日時")
    image = models.ImageField(
        upload_to="media/asovi_app/img", null=True, blank=True
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="favorite_user", on_delete=models.CASCADE
    )
    bakery = models.ForeignKey(
        Bakery, related_name="favorite_bakery", on_delete=models.PROTECT
    )
