from __future__ import absolute_import
from django.contrib import admin
from item.models import category, goods
# Register your models here.


from . import models

#admin.site.register(category)
#admin.site.register(goods)

admin.site.register(models.category)
admin.site.register(models.goods)
