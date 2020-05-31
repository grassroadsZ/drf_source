from django.db import models


# Create your models here.

class UserInfo(models.Model):
    user_types = (
        (1, 'Vip1'),
        (2, 'Vip2'),
        (3, 'Vip3'),
    )
    user_type = models.IntegerField(choices=user_types)
    username = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=60)


class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo", on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
