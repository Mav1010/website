from django.db import models


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseContactMessage(BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True