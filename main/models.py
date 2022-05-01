from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = "custom_user"
    # pass

    def __str__(self):
        return self.username


class Bakery(models.Model):
    name = models.CharField(verbose_name="店名", max_length=30)
    longitude = models.FloatField(verbose_name="経度")
    latitude = models.FloatField(verbose_name="緯度")
    info = models.TextField(verbose_name="詳細情報", null=True, blank=True)
    place_id = models.CharField(max_length=200, null=True, blank=True)
    added_at = models.DateTimeField(
        verbose_name="追加日時", auto_now_add=True, null=True, blank=True
    )

    def __str__(self):
        return self.name


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
        on_delete=models.SET_DEFAULT,
        verbose_name="店名"
    )
    comment = models.TextField(verbose_name="本文")
    pub_date = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)
    image = models.ImageField(
        upload_to="media/asovi_app/img", null=True, blank=True,
        verbose_name="写真"
    )

    def __str__(self):
        return f"from: {self.user}, to: {self.bakery}"


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="favorite_user", on_delete=models.CASCADE
    )
    bakery = models.ForeignKey(
        Bakery, related_name="favorite_bakery", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.user} saved {self.bakery}"
