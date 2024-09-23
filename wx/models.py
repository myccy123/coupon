from django.db import models


# Create your models here.
class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserInfo(BaseModel):
    GENDER = (
        ('male', '男'),
        ('female', '女'),
    )

    user_id = models.CharField(max_length=50, blank=True)
    openid = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    is_pay = models.BooleanField(default=False)
    idno = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=50, blank=True, choices=GENDER)
    tel = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    token = models.CharField(max_length=50, blank=True)
    avatar = models.FileField(upload_to='avatar', blank=True)
