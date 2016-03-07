# coding: utf-8
from __future__ import absolute_import
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import goods, category
from . import forms
from alipay.alipay import *
import hashlib
import time

#生成MD5加密字符串
def md5(value):
    zpl = hashlib.md5()
    zpl.update(value)
    return zpl.hexdigest()

def item_index(request):
    goods_cat = category.objects.all()
    goods_list = goods.objects.all()
    new_goods = goods.objects.order_by('add_time')[:4]
    hot_goods = goods.objects.order_by('click_count')[:4]
    return render(request, 'index.html', {
        'list':goods_list,
        'goods_cat':goods_cat,
        'new_goods':new_goods,
        'hot_goods':hot_goods
        })

def item_cat(request, cat_url):
    #cat = get_object_or_404(goods, cat_name="")
    #goods_list = goods.objects.all()
    caturl = cat_url
    goods_cat = category.objects.all()
    cid = category.objects.get(cat_url=cat_url).cat_id
    cat_name = category.objects.get(cat_url=cat_url).cat_name
    goods_list = goods.objects.filter(cat_id=cid)
    return render(request, 'list.html', {
        'list':goods_list,
        'goods_cat':goods_cat,
        'caturl':caturl,
        'cat_name':cat_name,
        })

def item_goods(request, pk):
    goods_cat = category.objects.all()
    post = get_object_or_404(goods, pk=pk)
    caturl = post.cat_id.cat_url
    cat_name = post.cat_id.cat_name
    return render(request, 'goods.html', {
        'post':post,
        'goods_cat':goods_cat,
        'caturl':caturl,
        'cat_name':cat_name,
        })


def payment(request):
    if request.method == 'POST':
        goods_size = request.POST.get('size')
        goods_color = request.POST.get('color')
        goods_number = int(request.POST.get('number'))
        goods_id = request.POST.get('goods_id')
        #使用当前系统时间 将时间戳转换成字符串 然后在使用MD5算法加密 保证tn的唯一性
        tn = md5(str(time.time()))
        zploo = get_object_or_404(goods, goods_id=goods_id)
        #return HttpResponse(tn)   #这是调试用的输出
        url = create_direct_pay_by_user (
                tn,  #唯一订单号
                zploo.goods_name,  #商品名称
                u'庄朋龙的商城',  #商品描述
                zploo.goods_price * goods_number,  #商品总价  单价*数量
                )
        return HttpResponseRedirect (url)
    else:
        return HttpResponse("违法操作")

#
def return_url_handler (request):
    '''用户付款后 支付宝返回的URL'''
    if notify_verify (request.GET):
        tn = request.GET.get('out_trade_no')   #唯一订单号
        trade_no = request.GET.get('trade_no')   #支付宝的交易号
        logger1.info('Change the status of bill %s'%tn)
        bill = Bill.objects.get (pk=tn)
        trade_status = request.GET.get('trade_status')   #交易状态 TRADE_SUCCESS 是交易成功,
        logger1.info('the status changed to %s'%trade_status)
        #将咱们系统里的订单交易状态 改成支付宝返回的 （支付宝返回TRADE_SUCCESS 就是 改成交易成功状态）
        bill.trade_status = trade_status
        upgrade_bill (bill, 30*6+7)  #升级  这是一个函数调用

        #确认用户已经付款后 就确认发货 （因为这是使用的即时到帐接口 所有就不用去发货了）
        #url=send_goods_confirm_by_platform (trade_no)
        #req=urllib.urlopen (url)
        #logger1.info('send goods confirmation. %s'%url)

        #为了照顾新手 就多写点注释  reverse()可有将列表的元素进行反向排序
        #HttpResponseRedirect 可以用来重定向（就是跳转的意思）
        return HttpResponseRedirect (reverse ('payment_success'))
    return HttpResponseRedirect (reverse ('payment_error'))

def payment_success(request):
    '''提示用户 已经支付完成'''
    return render(request, 'payment_success.html')

def payment_error(request):
    '''提示用户 支付失败'''
    return render(request, 'payment_error.html')


class CkEditorFormView(generic.FormView):
    form_class = forms.CkEditorForm
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('ckeditor-form')

ckeditor_form_view = CkEditorFormView.as_view()
