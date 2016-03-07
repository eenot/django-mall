# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# Create your models here.
class category(models.Model):
    """ 这是一个商品分类的模型 （数据库） """
    cat_id = models.AutoField(primary_key=True)  #分类的ID
    cat_name = models.CharField(max_length=90)  #分类的名称
    cat_url = models.CharField(max_length=60)  #分类的网址
    parent_id = models.SmallIntegerField( null=True, blank=True)  #分类的父类ID
    def __unicode__(self):
        return self.cat_name

class goods(models.Model):
    """ 这是goods商品表 """
    goods_id = models.AutoField(primary_key=True)  #商品的ID
    #商品名称
    goods_name = models.CharField(max_length=200)
    #商品的分类
    cat_id = models.ForeignKey(category)
    #商品的点击数
    click_count = models.IntegerField()
    #商品的售价
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    #商品的详细描述
    goods_desc = RichTextField()
    #goods_desc = models.TextField(null=True, blank=True)
    #商品的缩略图
    goods_thumb = models.CharField(max_length=255, null=True, blank=True)
    #商品原图
    goods_img = models.CharField(max_length=255, null=True, blank=True)
    #商品的添加时间
    add_time = models.DateTimeField(null=True, blank=True)
    #商品的最后更新时间
    last_update = models.DateTimeField(null=True, blank=True)
    #商品是否删除
    isdelete = models.BooleanField(default=False)
    def __unicode__(self):
        return self.goods_name
