#from django.template.loader import get_template
#from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from books.models import Book
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template import RequestContext
from selenium import webdriver
import time
from MyDJ.forms import ContactForm
from MyDJ.settings import BASE_DIR
import datetime
import os
import subprocess
import xlwt
from io import StringIO, BytesIO


def current_datetime0(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
def current_datetime1(request):
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
def current_datetime2(request):
    now = datetime.datetime.now()
    # Simple way of using templates from the filesystem.
    # This is BAD because it doesn't account for missing files!
    t = get_template('time.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
def current_datetime3(request):
    now = datetime.datetime.now()
    return render_to_response('time.html', {'current_date': now})
def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('time.html', locals())

def hours_ahead0(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
def hours_ahead(request, offset):
    hour_offset = int(offset)
    next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
    return render_to_response('plus.html', locals())

def display_meta0(request):
    values = request.META.items()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
def display_meta(request):
    values = request.META.items()
    return render_to_response('meta.html', locals())

def search_form(request):
    return render_to_response('search_form.html')

def search_results0(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
def search_results1(request):
    if 'q' in request.GET and request.GET['q']:
        query  = request.GET['q']
        books = Book.objects.filter(title__icontains=query)
        return render_to_response('search_results.html',locals())
    else:
        return HttpResponse('Please submit a search term.')
def search_results2(request):
    if 'q' in request.GET and request.GET['q']:
        query  = request.GET['q']
        books = Book.objects.filter(title__icontains=query)
        return render_to_response('search_results.html',locals())
    else:
        return render_to_response('search_form.html', {'error': True})
def search_results(request):
    errors = []
    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            errors.append('Enter a search term.')
        elif len(query) > 10:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=query)
            return render_to_response('search_results.html',locals())
    return render_to_response('search_form.html',{'errors': errors})


def contact0(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            # send_mail(   #服务器配置不完整，暂不能发送邮件
            #     request.POST['subject'],
            #     request.POST['message'],
            #     request.POST.get('email', 'noreply@example.com'),
            #     ['siteowner@example.com'],
            # )
            return HttpResponseRedirect('/thanks/')
    return render_to_response('contact_form.html',{
        'errors': errors,
        'subject': request.POST.get('subject', ''),
        'message': request.POST.get('message', ''),
        'email': request.POST.get('email', ''),
    },context_instance=RequestContext(request))
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send_mail(
            #     cd['subject'],
            #     cd['message'],
            #     cd.get('email', 'noreply@example.com'),
            #     ['siteowner@example.com'],
            # )
            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_form.html', {'form': form},context_instance=RequestContext(request))


def test(request):
    username = "weiqinlei" 
    return render_to_response('index.html',locals())


def expert_excel(request):
    errors = []
    if 'name' in request.GET:
        name = request.GET['name']
        if not name:
            errors.append('Enter a name.')
        else:
            name = os.path.join(BASE_DIR, 'File\\%s.xls' %name)
            style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
            style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
            wb = xlwt.Workbook()
            wb.encoding ='utf-8'
            ws = wb.add_sheet('Result')
            ws.write(0, 0, 'test', style0)
            ws.write(1, 0, datetime.datetime.now(), style1)
            ws.write(2, 0, 1)
            ws.write(2, 1, 1)
            ws.write(2, 2, xlwt.Formula("A3+B3"))
            ws.write(4, 2,33333)
            wb.save(name)
            return HttpResponseRedirect('/thanks/')
    return render_to_response('expert.html',{'errors': errors})
        

################################################################################################################
################################################################################################################
################################################################################################################
# 网页截屏函数 from selenium import webdriver
def capture(url, save_fn="captures.png"):
    browser = webdriver.Firefox() # Get local session of firefox
    browser.set_window_size(1200, 800)
    browser.get(url) # Load page
    browser.execute_script("""
        (function () {
          var y = 0;
          var step = 200;
          window.scroll(0, 0); 
          function f() {
            if (y < document.body.scrollHeight) {
              y += step;
              window.scroll(0, y);
              setTimeout(f, 100);
            } else {
              window.scroll(0, 0);
              document.title += "scroll-done";
            }
          } 
          setTimeout(f, 2000);
        })();
        """) 

    for i in range(30):
        if "scroll-done" in browser.title:
            break

    time.sleep(5) 
    browser.save_screenshot(save_fn)
    browser.close() 

if __name__ == "__main__":
    capture("http://www.baidu.com")

def capture_selenium(request):  ##  selenium —— django packet 通过pip或者下载安装
    errors = []
    if 'url' in request.GET:
        url = request.GET['url']
        if not url:
            errors.append('Enter a link.')
        else:
            capture(url)
            return HttpResponseRedirect('/thanks/')
    return render_to_response('capture.html',{'errors': errors})
################################################################################################################
def capture_screamshot(request):   ## screamshot —— django packet 通过pip或者下载安装  此方法暂时未实验成功
    errors = []
    if 'url' in request.GET:
        url = request.GET['url']
        if not url:
            errors.append('Enter a link.')
        else:
            return HttpResponseRedirect('/thanks/')
    return render_to_response('capture.html',{'errors': errors})
################################################################################################################
## 独立程序 直接运行phantomjs.exe截屏
## 通过此函数运行phantomjs.exe
def capture_phantomjs(request):  
    errors = []     
    if 'url' in request.GET:
        url = request.GET['url']
        if not url:
            errors.append('Enter a link.')
        else:
            file = datetime.datetime.now().strftime("%Y%m%d-%H%M%S");
            name = os.path.join(BASE_DIR, 'Capture\\%s.png' %file) 
            command = "phantomjs capture.js %s %s" %(url,name)
            subprocess.Popen(command, shell=True)
            return HttpResponseRedirect('/thanks/')
    return render_to_response('capture.html',{'errors': errors})
################################################################################################################
################################################################################################################
################################################################################################################

import socket

def findip(request): 
    rfile = open('MYDM.txt')
    wfile = open('MYIP.txt', 'w+')
    for line in rfile:
        str = line.strip().split(';')
        for s in str:
            s = s.strip().split('/')
            s = s[0]
            try:
                result = socket.gethostbyname(s)
            except:
                result = "error"
            if result == 'error':
                www = 'www'
                nPos = s.find(www)
                if nPos == -1:
                    s = 'www.' + s
                try:
                    result = socket.gethostbyname(s)
                except:
                    result = "0.0.0.0"
            wfile.write(result)
            wfile.write('\n')
            #print s
    rfile.close()
    wfile.close()
    return HttpResponseRedirect('/thanks/')
