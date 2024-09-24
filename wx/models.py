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


class PaymentInfo(BaseModel):
    openid = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    out_trade_no = models.CharField(max_length=50, blank=True)
    amount = models.FloatField(default=0)
    sp_appid = models.CharField(max_length=50, blank=True)
    sub_appid = models.CharField(max_length=50, blank=True)
    sp_mchid = models.CharField(max_length=50, blank=True)
    sub_mchid = models.CharField(max_length=50, blank=True)
    sp_openid = models.CharField(max_length=50, blank=True)
    sub_openid = models.CharField(max_length=50, blank=True)
    note = models.CharField(max_length=500, blank=True)
    res_content = models.TextField(blank=True)


class RefundInfo(BaseModel):
    refund_id = models.CharField(max_length=50, blank=True)
    out_refund_no = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    out_trade_no = models.CharField(max_length=50, blank=True)
    refund = models.FloatField(default=0)
    total = models.FloatField(default=0)
    sp_mchid = models.CharField(max_length=50, blank=True)
    sub_mchid = models.CharField(max_length=50, blank=True)
    note = models.CharField(max_length=500, blank=True)
    account = models.CharField(max_length=500, blank=True)
    res_content = models.TextField(blank=True)
