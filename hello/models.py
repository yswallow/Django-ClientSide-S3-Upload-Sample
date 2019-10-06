from django.db import models

from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Account(models.Model):
    username = models.CharField("ユーザー名", max_length=16)
    full_name = models.CharField("本名", max_length=128)
    avatar_url = models.URLField(verbose_name="アバター画像")
    
    @classmethod
    def update_account(cls, username, full_name, avatar_url):
        try:
            account = cls.objects.get(username=username)
        except(ObjectDoesNotExist):
            account = cls.objects.create()
            account.username = username
        account.full_name = full_name
        account.avatar_url = avatar_url
        account.save()
    
