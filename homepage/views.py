import mailtrap as mt
import random
import os
from .models import Mylogo,Image_news,Image_contact,Image_primaryschool,Image_register,Image_login,Image_t_c,Terms_and_Conditions,Partnership,Success_logo
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
import base64
import urllib.request
from unittest import loader
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, date
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.template import loader
from django.urls import resolve
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from payments.models import Payment_details
from django.contrib.auth.decorators import login_required
from .models import my_purchases,Books_Images,Videos,Price_list,add_basket,display_video
import stripe
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.db.models import Min
pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Verdana', 'fonts/verdana.ttf'))

stripe.api_key = settings.STRIPE_SECRET_KEY
def searchbar(request):
    if request.method == "POST":
        char = request.POST.get('search')
        found = Videos.objects.filter(chapter_title__iregex=char)
        if char=="":
            template = loader.get_template('searchbar.html')
            context = {
                'data': "",
            }
            return HttpResponse (template.render(context, request))
        elif not found.exists():
            template = loader.get_template('searchbar.html')
            context = {
                'data': "",
            }
            return HttpResponse (template.render(context, request))
        else:
            for i in found:
                refcode=i.ref_code_video
                general_info=Books_Images.objects.filter(ref_code_book=refcode)
            template = loader.get_template('searchbar.html')
            context = {
                'data': found,
                'gen_info':general_info,
                }
            return HttpResponse (template.render(context, request))
    else:
        return render(request,'searchbar.html')

@login_required
def books_image_view(request, *args, **kwargs):
    myurl=resolve(request.path_info).url_name
    mydata = Books_Images.objects.filter(ref_code=myurl).order_by('id')
    request.session['myurl'] = myurl
    template = loader.get_template('book_image.html')
    context = {
        'data': mydata,
        }
    return HttpResponse(template.render(context, request))

@login_required
def book_content(request,ref_code_book):
    url_context=request.build_absolute_uri()
    request.session['url_context'] =url_context
    ref_code_url=ref_code_book
    myurl = request.session.get('myurl')
    mydata=Books_Images.objects.filter(ref_code=myurl,ref_code_book=ref_code_url).values()
    book_title = mydata.values_list('book_title', flat=True).first()#
    request.session['book_title'] = book_title

    first_ids = Videos.objects.filter(ref_code=myurl,ref_code_video=ref_code_book).values('chapter_title').annotate(min_id=Min('id')).values_list('min_id', flat=True)
    list_capture = Videos.objects.filter(
        id__in=first_ids
    ).order_by('id').values_list('chapter_title', flat=True)
    
    template = loader.get_template('book_content.html')
    context = {
        'data': mydata,
        'list': list_capture,
        }
    return HttpResponse (template.render(context, request))
 
@login_required
def view_my_basket(request):
    url=request.session.get('url')
    userid=request.user.id
    mybasket=add_basket.objects.filter(username_id=userid)
    template = loader.get_template('my_basket.html')
    context = {
        'basket':mybasket,
        'url':url,
        }
    return HttpResponse(template.render(context, request))

@login_required
def my_purchases_items(request):
    userid=request.user.id
    mypurchases=my_purchases.objects.filter(username_id=userid)
    template = loader.get_template('my_purchases.html')
    context = {
        'purchases':mypurchases,
        }
    return HttpResponse(template.render(context, request))

def homepage(request):
    logo=Mylogo.objects.all()
    news_image=Image_news.objects.all()
    contact_image=Image_contact.objects.all()
    primary_image=Image_primaryschool.objects.all()
    login_image=Image_login.objects.all()
    register_image=Image_register.objects.all()
    t_c_image=Image_t_c.objects.all()
    part_ship=Partnership.objects.all()
    context = {'logo': logo,
               'news_image':news_image,
               'contact_image':contact_image,
               'primaryschool_image':primary_image,
               'login_image':login_image,
               'register_image':register_image,
               't_c_image':t_c_image,
               'Partnership':part_ship,
               }
    return render(request, 'homepage.html', context)

@csrf_exempt
def Terms_and_Condition(request):
    logo=Mylogo.objects.all()
    t_c=Terms_and_Conditions.objects.all()
    context = {
        't_c':t_c,
        'mylogo':logo,
        }
    return render(request, "t_c.html", context)

@login_required         
def lesson_details(request,ref_code_book):
    ref_code_url=ref_code_book
    request.session['ref_code_url'] =ref_code_url
    if request.method == "POST":
        char=request.POST.get('your_name')
        if char==None:
            messages.success(request, 'Σφάλμα: Παρακαλώ επιλέξτε μία από τις επιλογές που σας δίνονται!')
            return render(request,'error.html')
        else:
            checkout_data=Books_Images.objects.filter(ref_code_book=ref_code_book)#book-image
            my_data=Videos.objects.filter(ref_code_video=ref_code_book,chapter_title=char).order_by('sorting_video')#videos
            sum=my_data.values_list('chapter_title')#total videos per chapter
            total=0
            for i in sum:
                total=total+1
            if my_data.filter(stage='primary',chapter_title=char).exists():
                request.session['char'] =char
                request.session['ref_code_book']=ref_code_book
                now=timezone.now()
                costumer=request.user.id
                access = my_purchases.objects.filter(username_id=costumer)
                if request.user.is_superuser:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':char,
                        }
                    return HttpResponse(template.render(context, request))
                elif access.exists():
                    for i in access:
                        if i.end_date <now and i.chapter==char:
                            return HttpResponseRedirect(reverse('homepage:view_details'))
                        elif i.end_date>now and i.chapter==char:
                            template = loader.get_template('list_all_chapter.html')
                            context = {
                                'video': my_data,
                                'all': total,
                                'data': checkout_data,
                                'title':char,
                                }
                            return HttpResponse(template.render(context, request))
                
                        elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                            template = loader.get_template('list_all_chapter.html')
                            context = {
                                'video': my_data,
                                'all': total,
                                'data': checkout_data,
                                'title':char,
                                }
                            return HttpResponse(template.render(context, request))
                        else:
                            return HttpResponseRedirect(reverse('homepage:view_details'))
                            
                else:
                    return HttpResponseRedirect(reverse('homepage:view_details'))
    
            elif my_data.filter(stage='secondary',chapter_title=char).exists():
                request.session['char'] =char
                request.session['ref_code_book']=ref_code_book
                now=timezone.now()
                costumer=request.user.id
                access = my_purchases.objects.filter(username_id=costumer)
                if request.user.is_superuser:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':char,
                        }
                    return HttpResponse(template.render(context, request))
        
                if access.exists():
                    for i in access:
                        if i.end_date <now and i.chapter==char:
                            return HttpResponseRedirect(reverse('homepage:view_details'))
                
                        elif i.end_date>now and i.chapter==char:
                            template = loader.get_template('list_all_chapter.html')
                            context = {
                                'video': my_data,
                                'all': total,
                                'data': checkout_data,
                                'title':char,
                                }
                            return HttpResponse(template.render(context, request))
                
                        elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                            template = loader.get_template('list_all_chapter.html')
                            context = {
                                'video': my_data,
                                'all': total,
                                'data': checkout_data,
                                'title':char,
                                }
                            return HttpResponse(template.render(context, request))
                        else:
                            return HttpResponseRedirect(reverse('homepage:view_details'))
                        
                else:
                    return HttpResponseRedirect(reverse('homepage:view_details'))
                
            elif my_data.filter(stage='high',chapter_title=char).exists():
                request.session['char'] =char
                request.session['ref_code_book']=ref_code_book
                now=timezone.now()
                costumer=request.user.id
                access = my_purchases.objects.filter(username_id=costumer)
                if request.user.is_superuser:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':char,
                        }
                    return HttpResponse(template.render(context, request))
                if access.exists():
                    if request.user.is_superuser:
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': my_data,
                            'all': total,
                            'data': checkout_data,
                            'title':char,
                            }
                        return HttpResponse(template.render(context, request))
                    else:
                        for i in access:
                            if i.end_date <now and i.chapter==char:
                                return HttpResponseRedirect(reverse('homepage:view_details'))
                    
                            elif i.end_date>now and i.chapter==char:
                                template = loader.get_template('list_all_chapter.html')
                                context = {
                                    'video': my_data,
                                    'all': total,
                                    'data': checkout_data,
                                    'title':char,
                                    }
                                return HttpResponse(template.render(context, request))
                    
                            elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                                template = loader.get_template('list_all_chapter.html')
                                context = {
                                    'video': my_data,
                                    'all': total,
                                    'data': checkout_data,
                                    'title':char,
                                    }
                                return HttpResponse(template.render(context, request))
                    
                            else:
                                return HttpResponseRedirect(reverse('homepage:view_details'))
                        
                else:
                    return HttpResponseRedirect(reverse('homepage:view_details'))
    
            else:
                char=='Παρακολούθηση όλων των Κεφαλαίων'
                request.session["char"] = char
                request.session["ref_code_book"] = ref_code_book
                primary_all_chapter = Videos.objects.filter(ref_code_video=ref_code_book, stage='primary').order_by('id')
                sec_all_chapter=Videos.objects.filter(ref_code_video=ref_code_book,stage='secondary').order_by('id')
                high_all_chapter=Videos.objects.filter(ref_code_video=ref_code_book,stage='high').order_by('id')
                sum1=primary_all_chapter.values_list('chapter_title')
                sum2=sec_all_chapter.values_list('chapter_title')
                sum3=high_all_chapter.values_list('chapter_title')#total videos per chapter
                total=0
                if primary_all_chapter.exists():
                    primary_chapter = (primary_all_chapter.values('chapter_title', 'part_title', 'part_video','id').order_by('chapter_title', 'part_title', 'part_video','id').distinct('chapter_title'))
                    now=timezone.now()
                    costumer=request.user.id
                    access = my_purchases.objects.filter(username_id=costumer,chapter=char)
                    if request.user.is_superuser:
                        chapt_list=[]
                        for i in sum1:
                            chapt_list.append(i)
                        total=len(set(chapt_list))
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': primary_chapter,
                            'all': total,
                            'data': checkout_data,
                            'title':char,
                            'check':1,
                            }
                        return HttpResponse(template.render(context, request))
                    elif access.exists():
                        for i in access:  
                            if i.end_date >now and i.chapter==char:
                                chapt_list=[]
                                for i in sum1:
                                    chapt_list.append(i)
                                total=len(set(chapt_list))
                                template = loader.get_template('list_all_chapter.html')
                                context = {
                                    'video': primary_chapter,
                                    'all': total,
                                    'data': checkout_data,
                                    'title':char,
                                    'check':1,
                                    }
                                return HttpResponse(template.render(context, request))
                            else:
                                return HttpResponseRedirect(reverse('homepage:view_details'))
                    else:
                        return HttpResponseRedirect(reverse('homepage:view_details'))
        
                elif sec_all_chapter.exists():
                    sec_chapter = (sec_all_chapter.values('chapter_title', 'part_title', 'part_video').order_by('chapter_title', 'part_title', 'part_video').distinct('chapter_title'))
                    now=timezone.now()
                    costumer=request.user.id
                    access = my_purchases.objects.filter(username_id=costumer,chapter=char)
                    if request.user.is_superuser:
                        chapt_list=[]
                        for i in sum2:
                            chapt_list.append(i)
                        total=len(set(chapt_list))
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': sec_chapter,
                            'all': total,
                            'data': checkout_data,
                            'title':char,
                            'check':1,
                            }
                        return HttpResponse(template.render(context, request))
                    elif access.exists():
                        for i in access:  
                            if i.end_date >now and i.chapter==char:
                                chapt_list=[]
                                for i in sum2:
                                    chapt_list.append(i)
                                total=len(set(chapt_list))
                                template = loader.get_template('list_all_chapter.html')
                                context = {
                                    'video': sec_chapter,
                                    'all': total,
                                    'data': checkout_data,
                                    'title':char,
                                    'check':1,
                                    }
                                return HttpResponse(template.render(context, request))
                            else:
                                return HttpResponseRedirect(reverse('lesson_details:view_details'))
                    else:
                        return HttpResponseRedirect(reverse('lesson_details:view_details'))
                                        
                elif high_all_chapter .exists():
                    high_chapter = (sec_all_chapter.values('chapter_title', 'part_title', 'part_video').order_by('chapter_title', 'part_title', 'part_video').distinct('chapter_title'))
                    now=timezone.now()
                    costumer=request.user.id
                    access = my_purchases.objects.filter(username_id=costumer,chapter=char)
                    if request.user.is_superuser:
                        chapt_list=[]
                        for i in sum3:
                            chapt_list.append(i)
                        total=len(set(chapt_list))
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': high_chapter,
                            'all': total,
                            'data': checkout_data,
                            'title':char,
                            'check':1,
                            }
                        return HttpResponse(template.render(context, request))
                    if access.exists():
                        for i in access:  
                            if i.end_date >now and i.chapter==char:
                                chapt_list=[]
                                for i in sum3:
                                    chapt_list.append(i)
                                total=len(set(chapt_list))
                                template = loader.get_template('list_all_chapter.html')
                                context = {
                                    'video': high_chapter,
                                    'all': total,
                                    'data': checkout_data,
                                    'title':char,
                                    'check':1,
                                    }
                                return HttpResponse(template.render(context, request))
                            else:
                                return HttpResponseRedirect(reverse('lesson_details:view_details'))
                    else:
                        return HttpResponseRedirect(reverse('lesson_details:view_details'))
                else:
                    return HttpResponseRedirect(reverse('lesson_details:view_details'))
    else:
        messages.success(request, 'Σφάλμα: Παρακαλώ επιλέξτε μία από τις επιλογές που σας δίνονται!')
        return render(request,'error.html')

@login_required 
def view_details(request):
    ref_code_book=request.session.get('ref_code_book')
    char=request.session.get('char')
    
    whatincludes=Videos.objects.filter(ref_code_video=ref_code_book,chapter_title=char).order_by('sorting_video')
    
    checkout_data=Books_Images.objects.filter(ref_code_book=ref_code_book)#book-image
    
    checkout_price_chapter=Price_list.objects.filter(ref_code_video=ref_code_book,title=char).values('price_chapter')
    
    checkout_price_all_book=Price_list.objects.filter(ref_code_video=ref_code_book).values('price_all_book').distinct()
    price_chapter_sum = sum(filter(None,checkout_price_chapter.values_list('price_chapter', flat=True)))
    price_all_book_sum = sum(filter(None,checkout_price_all_book.values_list('price_all_book', flat=True)))
    price_chapter=int(price_chapter_sum)
    price_all_book=int(price_all_book_sum)
    
    my_data=Videos.objects.filter(ref_code_video=ref_code_book,chapter_title=char).order_by('id')#videos
    sum_value=my_data.values_list('chapter_title')#total videos per chapter
    total=0
    for i in sum_value:
        total=total+1
    if my_data.filter(stage='primary',chapter_title=char).exists():
        url=request.build_absolute_uri()
        request.session['url'] =url
        template = loader.get_template('lesson_details.html')
        context = {
            'chapter':char,
            'data': checkout_data,
            'total':total,
            'ref_code_book':ref_code_book,
            'price':price_chapter,
            'what_includes':whatincludes,
            }
        return HttpResponse(template.render(context, request))   
    
    elif my_data.filter(stage='secondary',chapter_title=char).exists():
        url=request.build_absolute_uri()
        request.session['url'] =url
        template = loader.get_template('lesson_details.html')
        context = {
            'chapter':char,
            'data': checkout_data,
            'total':total,
            'ref_code_book':ref_code_book,
            'price':price_chapter,
            'what_includes':whatincludes,
            }
        return HttpResponse(template.render(context, request))
        
    elif my_data.filter(stage='high',chapter_title=char).exists():
        url=request.build_absolute_uri()
        request.session['url'] =url
        template = loader.get_template('lesson_details.html')
        context = {
            'chapter':char,
            'data': checkout_data,
            'total':total,
            'ref_code_book':ref_code_book,
            'price':price_chapter,
            'what_includes':whatincludes,
            }
        return HttpResponse(template.render(context, request))
    
    elif char=='Παρακολούθηση όλων των Κεφαλαίων':
        whatincludes=Videos.objects.filter(ref_code_video=ref_code_book).order_by('id')
        primary_all_chapter=Videos.objects.filter(ref_code_video=ref_code_book,stage='primary')
        sec_all_chapter=Videos.objects.filter(ref_code_video=ref_code_book,stage='secondary')
        high_all_chapter=Videos.objects.filter(ref_code_video=ref_code_book,stage='high')
        sum1=primary_all_chapter.values_list('chapter_title')
        sum2=sec_all_chapter.values_list('chapter_title')
        sum3=high_all_chapter.values_list('chapter_title')#total videos per chapter
        total=0
        if primary_all_chapter.exists():
            url=request.build_absolute_uri()
            request.session['url'] =url
            chapt_list=[]
            for i in sum1:
                chapt_list.append(i)
            total=len(set(chapt_list))
            template = loader.get_template('lesson_details.html')
            context = {
                'chapter':char,
                'data': checkout_data,
                'all':total,
                'check':1,
                'ref_code_book':ref_code_book,
                'price':price_all_book,
                'what_includes':whatincludes,
                }
            return HttpResponse(template.render(context, request))
                  
        elif sec_all_chapter.exists():
            url=request.build_absolute_uri()
            request.session['url'] =url
            chapt_list=[]
            for i in sum2:
                chapt_list.append(i)
            total=len(set(chapt_list))
            template = loader.get_template('lesson_details.html')
            context = {
                'chapter':char,
                'data': checkout_data,
                'all':total,
                'check':1,
                'ref_code_book':ref_code_book,
                'price':price_all_book,
                'what_includes':whatincludes,
                }
            return HttpResponse(template.render(context, request))
                        
        else:
            high_all_chapter.exists()
            url=request.build_absolute_uri()
            request.session['url'] =url
            chapt_list=[]
            for i in sum3:
                chapt_list.append(i)
            total=len(set(chapt_list))
            template = loader.get_template('lesson_details.html')
            context = {
                'chapter':char,
                'data': checkout_data,
                'all':total,
                'check':1,
                'ref_code_book':ref_code_book,
                'price':price_all_book,
                'what_includes':whatincludes,
                }
            return HttpResponse(template.render(context, request))

@login_required
def check_out_payment(request):
    costumer=request.user.id
    data_list=add_basket.objects.filter(username_id=costumer).values()
    price_cost=sum(data_list.values_list('price', flat=True))
    request.session['price'] = int(price_cost)
    book_discr=data_list.values_list('book_title', flat=True)
    chapter_discr=data_list.values_list('chapter', flat=True)
    result_list_book_discr = [str(obj) for obj in book_discr]
    result_list_chapter_discr = [str(obj) for obj in chapter_discr]
    result_book_discr = '\n, '.join(result_list_book_discr)
    result_chapter_discr = '\n, '.join(result_list_chapter_discr)
    if not price_cost:
        a=messages.error(request, 'Το Καλάθι σας είναι άδειο! Παρακαλώ καταχωρήστε στο καλάθι σας το μάθημα που επιθυμείτε για παρακολούθηση!')
        template = loader.get_template('error_empty_basket.html')
        context = {
            'error':a,      
        }
        return HttpResponse(template.render(context, request))
    else:
        try:
            currency = 'eur'
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                       'currency': currency,
                        'unit_amount': int(price_cost * 100),  # Convert to cents
                        'product_data': {
                            'name': result_book_discr,
                            'description': result_chapter_discr,
                        # You can add images here as well using 'images': ['image_url'],
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('https://www.cpnetuni.com/pay_success/'),
                cancel_url=request.build_absolute_uri('https://www.cpnetuni.com/pay_cancel/'),
            )
            payment_url = session.url
        except stripe.error.StripeError as e:
            payment_url = session.cancel_url
            error_message = e.error.message
            return render(request, 'payment_error.html', {'error_message': error_message})

        return redirect(payment_url)

@login_required
def add_basket_item(request,ref_code_book,chapter,price):
    url=request.session.get('url')
    costumer=request.user.id
    image=Books_Images.objects.filter(ref_code_book=ref_code_book)
    part=Videos.objects.filter(ref_code_video=ref_code_book)
    for i in image:
        for j in part:
           image1=i.image
           book_title=i.book_title
           part=j.part_video
    exist=add_basket.objects.filter(username_id=costumer).values()
    exist_true=exist.filter(chapter=chapter,videos_url=ref_code_book).values()
    if exist_true:
        msg='***Το μάθημα υπάρχει στο καλάθι σας'
        messages.error(request,msg)
        return redirect(url)
    else:
        basket_added = add_basket( username_id=costumer, chapter=chapter,videos_url=ref_code_book,image=image1,book_title=book_title, price=price,part=part)
        basket_added.save()
        return redirect(url)#παραμένει στην ίδια σελίδα

@login_required
def my_basket(request,chapter,videos_url):#μεσω url στο html αν
    
    checkout_data=Books_Images.objects.filter(ref_code_book=videos_url)#book-image
    my_data=Videos.objects.filter(ref_code_video=videos_url,chapter_title=chapter).order_by('chapter_title')#videos
    sum=my_data.values_list('chapter_title')#total videos per chapter
    total=0
    for i in sum:
        total=total+1
    
    if my_data.filter(stage='primary',chapter_title=chapter).exists():
        request.session["char"] = chapter
        request.session["ref_code_book"] = videos_url
        now=timezone.now()
        costumer=request.user.id
        access = my_purchases.objects.filter(username_id=costumer)
        
        if access.exists():
            for i in access:
                if i.end_date <now and i.chapter==chapter:
                   return HttpResponseRedirect(reverse('homepage:view_details'))
                
                elif i.end_date>now and i.chapter==chapter:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter,
                        }
                    return HttpResponse(template.render(context, request))
                
                elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter,
                        }
                    return HttpResponse(template.render(context, request))
                
                else:
                    return HttpResponseRedirect(reverse('lesson_details:view_details'))             
        else:
            return HttpResponseRedirect(reverse('lesson_details:view_details'))
    
    elif my_data.filter(stage='secondary',chapter_title=chapter).exists():
        request.session["char"] = chapter
        request.session["ref_code_book"] = videos_url
        now=timezone.now()
        costumer=request.user.id
        access = my_purchases.objects.filter(username_id=costumer)
        
        if access.exists():
            for i in access:
                if i.end_date <now and i.chapter==chapter:
                   return HttpResponseRedirect(reverse('lesson_details:view_details'))
                
                elif i.end_date>now and i.chapter==chapter:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter,
                        }
                    return HttpResponse(template.render(context, request))
                
                elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter,
                        }
                    return HttpResponse(template.render(context, request))
                
                else:
                    return HttpResponseRedirect(reverse('lesson_details:view_details'))             
        else:
            return HttpResponseRedirect(reverse('lesson_details:view_details'))
        
    elif my_data.filter(stage='high',chapter_title=chapter).exists():
        request.session["char"] = chapter
        request.session["ref_code_book"] = videos_url
        now=timezone.now()
        costumer=request.user.id
        access = my_purchases.objects.filter(username_id=costumer)
        
        if access.exists():
            for i in access:
                if i.end_date <now and i.chapter==chapter:
                   return HttpResponseRedirect(reverse('lesson_details:view_details'))
                
                elif i.end_date>now and i.chapter==chapter:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter,
                        }
                    return HttpResponse(template.render(context, request))
                
                elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter,
                        }
                    return HttpResponse(template.render(context, request))
                
                else:
                    return HttpResponseRedirect(reverse('lesson_details:view_details'))
                        
        else:
            return HttpResponseRedirect(reverse('lesson_details:view_details'))
    
    elif chapter=='Παρακολούθηση όλων των Κεφαλαίων':
        request.session["char"] = chapter
        request.session["ref_code_book"] = videos_url
        primary_all_chapter=Videos.objects.filter(ref_code_video=videos_url,stage='primary').values_list('chapter_title', flat=True).distinct()
        sec_all_chapter=Videos.objects.filter(ref_code_video=videos_url,stage='secondary').values_list('chapter_title', flat=True).distinct()
        high_all_chapter=Videos.objects.filter(ref_code_video=videos_url,stage='high').values_list('chapter_title', flat=True).distinct()
        sum1=primary_all_chapter.values_list('chapter_title')
        sum2=sec_all_chapter.values_list('chapter_title')
        sum3=high_all_chapter.values_list('chapter_title')#total videos per chapter
        total=0
        if primary_all_chapter.exists():
            primary_chapter = (primary_all_chapter.values('chapter_title', 'part_title', 'part_video').order_by('chapter_title', 'part_title', 'part_video').distinct('chapter_title'))
            now=timezone.now()
            costumer=request.user.id
            access = my_purchases.objects.filter(username_id=costumer,chapter=chapter)
            if access.exists():
                for i in access:  
                    if i.end_date >now and i.chapter==chapter:
                        chapt_list=[]
                        for i in sum1:
                            chapt_list.append(i)
                        total=len(set(chapt_list))
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': primary_chapter,
                            'all': total,
                            'data': checkout_data,
                            'title':chapter,
                            'check':1,
                            }
                        return HttpResponse(template.render(context, request))
                    else:
                        return HttpResponseRedirect(reverse('lesson_details:view_details'))
            else:
                return HttpResponseRedirect(reverse('lesson_details:view_details'))
        
        elif sec_all_chapter.exists():
            sec_chapter = (sec_all_chapter.values('chapter_title', 'part_title', 'part_video').order_by('chapter_title', 'part_title', 'part_video').distinct('chapter_title'))
            now=timezone.now()
            costumer=request.user.id
            access = my_purchases.objects.filter(username_id=costumer,chapter=chapter)
            if access.exists():
                for i in access:  
                    if i.end_date >now and i.chapter==chapter:
                        chapt_list=[]
                        for i in sum2:
                            chapt_list.append(i)
                        total=len(set(chapt_list))
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': sec_chapter,
                            'all': total,
                            'data': checkout_data,
                            'title':chapter,
                            'check':1,
                            }
                        return HttpResponse(template.render(context, request))
                    else:
                        return HttpResponseRedirect(reverse('lesson_details:view_details'))
            else:
                return HttpResponseRedirect(reverse('lesson_details:view_details'))
                                        
        elif high_all_chapter .exists():
            high_chapter = (high_all_chapter.values('chapter_title', 'part_title', 'part_video').order_by('chapter_title', 'part_title', 'part_video').distinct('chapter_title'))
            now=timezone.now()
            costumer=request.user.id
            access = my_purchases.objects.filter(username_id=costumer,chapter=chapter)
            if access.exists():
                for i in access:  
                    if i.end_date >now and i.chapter==chapter:
                        chapt_list=[]
                        for i in sum3:
                            chapt_list.append(i)
                        total=len(set(chapt_list))
                        template = loader.get_template('list_all_chapter.html')
                        context = {
                            'video': high_chapter,
                            'all': total,
                            'data': checkout_data,
                            'title':chapter,
                            'check':1,
                            }
                        return HttpResponse(template.render(context, request))
                    else:
                        return HttpResponseRedirect(reverse('lesson_details:view_details'))
            else:
                return HttpResponseRedirect(reverse('lesson_details:view_details'))

@login_required
def delete(request, id):
  userid=request.user.id
  add_basket.objects.filter(username_id=userid,id=id).delete()
  return HttpResponseRedirect(reverse('homepage:view_my_basket'))#παραμένει στην ίδια σελίδα 

@login_required
def show_video(request,chapter_title,part_title,part_video):
    my_data = Videos.objects.filter(chapter_title=chapter_title,part_title=part_title,part_video=part_video).order_by('sorting_video')
    all_part_video=Videos.objects.filter(chapter_title=chapter_title).order_by('sorting_video')
    for i in my_data:
        y=i.views
        i.views=y+1
        i.save()
    for i in my_data:
        onedrive_link = str(i.video)
    response = urllib.request.urlopen(onedrive_link)
    video_content = response.read()
    encoded_video_data = base64.b64encode(video_content).decode('utf-8')
    data_url = f'data:video/mp4;base64,{encoded_video_data}'
    context = {
        'data': my_data,
        'data_url':data_url,
        'all_part_video':all_part_video,
        }
    return render(request, 'display_video.html', context)

@csrf_exempt
def add_whachtime(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        chapter_title = data.get('chapter_title', False)
        part_video = data.get('part_video', False)
        video_ended = data.get('video_ended', False)
        time = data.get('time', '00:00:00')
         
        
        now=timezone.now()
        now_db=now.date().today()
        costumer=request.user.id
        book=my_purchases.objects.filter(username_id=costumer,chapter=chapter_title)
        if book.exists():
            for i in book:
                title=i.book_title
                x=display_video(username_id=costumer,book_title=title,chapter=chapter_title,part=part_video,display_date=now_db,watch=video_ended,duration=time)
                x.save()
        else:
            book_title = request.session.get('book_title')
            x=display_video(username_id=costumer,book_title=book_title,chapter=chapter_title,part=part_video,display_date=now_db,watch=video_ended,duration=time)
            x.save()
        return HttpResponse(status=204)

        
        #exist_access.objects.filter(username_id=costumer,videos_url=video_url).update(watch=watch)

@login_required
def pay_success(request):
    costumer=request.user.id
    add_items_from_basket=add_basket.objects.filter(username_id=costumer)
    now=datetime.now()
    exbire=now.replace(now.year + 1)
    for item in add_items_from_basket:
        success=my_purchases(username_id=costumer, videos_url=item.videos_url,  created_date=now,  end_date=exbire, chapter=item.chapter,book_title=item.book_title, price=item.price, image=item.image,part=item.part)
        success.save()
    #basket.objects.filter(username_id=costumer).delete()
    return HttpResponseRedirect(reverse("homepage:create_invoice")) 

@login_required
def pay_cancel(request):
    return render(request,'payment_error.html')

@login_required
def create_invoice(request):
    costumer=request.user.id
    print_out=add_basket.objects.filter(username_id=costumer)
    now=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    current_date = date.today()
    rec_num=random.randint(10000000,999999999)
    rec_num_str=str(rec_num)
    fname = request.user.first_name
    lname = request.user.last_name
    email = request.user.email
    filename=rec_num_str+'_'+'invoice_C.P.pdf'
    company_name = "C.P Education for All"
    image='https://res.cloudinary.com/hewckvlra/image/upload/v1738511213/mylogo_b1prnw.png'
    #-------------------------------------create invoice
    data=["Μάθημα" , "Κεφάλαιο" , "Τιμή"]
    
#---------------------------------------
    pdf = canvas.Canvas(filename, pagesize=A4)
    
#----------------------------------
#logo
    pdf.drawInlineImage(image,30,750,425,60)
#----------------------------
#pdf.setTitle('invoice')
    pdf.line(15, 630, 575, 630)
    pdf.setFillColor(colors.black)
    pdf.setFont('Verdana',30)
    pdf.drawString(150, 600, 'Απόδειξη Πληρωμής')
    pdf.line(15, 590, 575, 590)
#pdf.line(33, 650, 170, 650)

    pdf.setFillColor(colors.black)
    pdf.setFont('Verdana',14)
    pdf.drawString(30,560,'Στοιχεία Πελάτη')
    pdf.line(30, 555, 140, 555)

    pdf.setFillColor(colors.black)
    pdf.setFont('Verdana',12)
    pdf.drawString(30,525,'Ονοματεπώνυμο: '+fname + ' '+ lname)
    pdf.drawString(30,505,'Email: '+email)
    pdf.setFillColor(colors.blue)
    pdf.drawString(30,485,'Αποδοχή όρων και προϋποθέσεων')
    pdf.setFillColor(colors.black)
    pdf.drawString(30,465,'Τρόπος Πληρωμής:')
    pdf.setFillColor(colors.blue)
    pdf.drawString(150,465,'online payment')
#----------------------------------------
    pdf.setFillColor(colors.red)
    pdf.drawString(360,720,company_name)
    pdf.setFillColor(colors.black)
    pdf.setFont('Verdana',12)
    pdf.drawString(360,700,'Αριθ.Απόδειξης: ')
    pdf.setFillColor(colors.blue)
    pdf.drawString(460,700,str(rec_num))
    pdf.setFillColor(colors.black)
    pdf.drawString(360,680,'Ημερομηνία: '+str(now))
    pdf.drawString(360,660,'Email:cpnetunicy@outlook.com')
    
#----------------------------------------
    pdf.setFillColor(colors.black)
    pdf.setFont('DejaVuSans',14)
    pdf.line(15, 440, 580, 440)
    tab=30
    for i in range(len(data)):
        if i==1:
            tab=225
            pdf.drawString(tab,400,str(data[i]))
        elif i==2:
            pdf.drawString(tab+285,400,str(data[i]))
        else:
            pdf.drawString(tab,400,str(data[i]))
#---------------------------------------------------
    ipsos=380
    amount=0
    price_amount=''
    for i in print_out:
        title=i.book_title
        chapter=i.chapter
        price=str(i.price)
        pdf.setFillColor(colors.black)
        pdf.setFont('DejaVuSans',8)
        pdf.drawString(30,ipsos,title)
        pdf.drawString(225,ipsos,chapter)
        pdf.drawString(510,ipsos,'€'+price)
        ipsos=ipsos-25
        title=''
        chapter=''
        price=''
        amount=amount+i.price
    price_amount=str(amount)
    pdf.drawString(475,ipsos,'Σύνολο: €')
    pdf.drawString(515,ipsos,price_amount)
    pdf.line(15, ipsos-20, 580, ipsos-20)
    store="invoices/{0}/".format(str(current_date))
    path=store+filename
    os.makedirs(store, exist_ok=True)
    pdf.showPage()
    pdf.save()
    if os.path.exists(filename):
        os.rename(filename,path)
    #---------------------------------email
    text_value=''
    count=0
    for i in print_out:
        text_value=text_value+' '+i.book_title+':'+' '+i.chapter+'\n'
        count=count+1
    if count >1:
        text='Σας ευχαριστούμε που επιλέξατε το C.P Education for All. Πιο κάτω επισυνάπτεται η απόδειξη αγοράς των φροντιστηριακών μαθημάτων: {}'.format('\n'+text_value)
    else:
        text='Σας ευχαριστούμε που επιλέξατε το C.P Education for All. Πιο κάτω επισυνάπτεται η απόδειξη αγοράς του φροντιστηριακού μαθήματος: {}'.format('\n'+text_value)

    with open(path, "rb") as pdf_file:
        pdf_content = pdf_file.read()
    pdf_base64 = base64.b64encode(pdf_content)

    pdf_attachment = mt.Attachment(
        content=pdf_base64,
        filename=filename,  # Replace with the desired filename
        mimetype="application/pdf",  # PDF MIME type
    )

    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@cpnetuni.com", name="Απόδειξη Πληρωμής Φροντιστηριακού Μαθήματος"),
        to=[mt.Address(email=email)],
        bcc=[mt.Address('cpnetuni@gmail.com')],
        subject='Απόδειξη Πληρωμής Φροντιστηριακού Μαθήματος',
        text=text,
        category="Αποδείξεις",
    )

    mail.attachments = [pdf_attachment]
    client = mt.MailtrapClient(token="388ed30f960c9bd511b4cbd740d05b7d")
    client.send(mail)

    add_basket.objects.filter(username_id=costumer).delete()
    successlogo=Success_logo.objects.all()
    os.remove(path)
    return render(request,"homepage/success_payment.html",{'logo':successlogo})

@login_required         
def lesson_details_searchbar(request,ref_code_book,chapter_title):
    ref_code_url=ref_code_book
    request.session['ref_code_url'] =ref_code_url
    if request.method == "POST":
        char=request.POST.get('your_name')
        if char==None:
            messages.success(request, 'Σφάλμα: Παρακαλώ επιλέξτε μία από τις επιλογές που σας δίνονται!')
            return render(request,'error.html')
        
    checkout_data=Books_Images.objects.filter(ref_code_book=ref_code_book)#book-image
    my_data=Videos.objects.filter(ref_code_video=ref_code_book,chapter_title=chapter_title).order_by('sorting_video')#videos
    sum=my_data.values_list('chapter_title')#total videos per chapter
    chapter=chapter_title
    total=0
    for i in sum:
        total=total+1
    
    if my_data.filter(stage='primary',chapter_title=chapter_title).exists():
        template = loader.get_template('list_all_chapter.html')
        context = {
            'video': my_data,
            'all': total,
            'data': checkout_data,
            'chapter':chapter,
            }
        return HttpResponse(template.render(context, request))
    
    elif my_data.filter(stage='secondary',chapter_title=chapter_title).exists():
        now=timezone.now()
        costumer=request.user.id
        access = my_purchases.objects.filter(username_id=costumer)
        
        if access.exists():
            for i in access:
                if i.end_date <now and i.chapter==chapter_title:
                   return HttpResponseRedirect(reverse('lesson_details:view_details'))
                
                elif i.end_date>now and i.chapter==chapter_title:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter_title,
                        }
                    return HttpResponse(template.render(context, request))
                
                elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter_title,
                        }
                    return HttpResponse(template.render(context, request))
                
                else:
                    return HttpResponseRedirect(reverse('lesson_details:view_details'))
                        
        else:
            return HttpResponseRedirect(reverse('lesson_details:view_details'))
    
    elif my_data.filter(stage='high',chapter_title=chapter_title).exists():
        now=timezone.now()
        costumer=request.user.id
        access = my_purchases.objects.filter(username_id=costumer)
        
        if access.exists():
            for i in access:
                if i.end_date <now and i.chapter==chapter_title:
                   return HttpResponseRedirect(reverse('lesson_details:view_details'))
                
                elif i.end_date>now and i.chapter==chapter_title:
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter_title,
                        }
                    return HttpResponse(template.render(context, request))
                
                elif i.end_date>now and i.chapter=='Παρακολούθηση όλων των Κεφαλαίων':
                    template = loader.get_template('list_all_chapter.html')
                    context = {
                        'video': my_data,
                        'all': total,
                        'data': checkout_data,
                        'title':chapter_title,
                        }
                    return HttpResponse(template.render(context, request))
                
                else:
                    return HttpResponseRedirect(reverse('lesson_details:view_details'))
                        
        else:
            return HttpResponseRedirect(reverse('lesson_details:view_details'))