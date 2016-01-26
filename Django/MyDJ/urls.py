from django.contrib.staticfiles.urls import staticfiles_urlpatterns  
from django.contrib import admin
from django.conf.urls import patterns, url, include
#from django.views.generic import list_detail
from django.views.generic import ListView, DetailView
from MyDJ import views
from MyDJ import settings
from books.models import Publisher

admin.autodiscover()

publisher_info = {
    'queryset': Publisher.objects.all(),
    'template_name': 'publisher_list_page.html',
    'template_object_name': 'publisherlist',
}
publisherinfo = ListView.as_view( 
        queryset=Publisher.objects.all(),
        context_object_name='publisherlist',
        template_name='publisher_list_page.html')

urlpatterns = patterns('',     
    (r'^admin/', include(admin.site.urls)),    
    (r'^time/$', views.current_datetime),
    (r'^time/plus/(\d{1,2})/$', views.hours_ahead),
    (r'^meta/$', views.display_meta),
    (r'^search_form/$', views.search_form),
    (r'^search_results/$', views.search_results),
    (r'^search/$', views.search_results),
    (r'^capture/$',views.capture_phantomjs),
    (r'^capture_selenium/$', views.capture_selenium),
    (r'^excel/$', views.expert_excel),
    (r'^findip/$', views.findip),
    # (r'^contact/$', views.contact),  
    # (r'^contact/thanks/$', views.test),    
)

urlpatterns += patterns('MyDJ.views',      #字符串技术  +=
    (r'^contact/$', 'contact'),            #函数也加''  等价于views.contact
    (r'^thanks/$', 'test'),    
)

#**************************通用视图解决方案******************************#  
urlpatterns += patterns('',      
    #*************************（方案一  无效）***************************#    
    # (r'^publishers/$', list_detail.object_list, publisher_info), 
    # 此方案无效，因为from django.views.generic import list_detail不存在
    #********************************************************************#    
    #****************************（方案二）******************************# 
    # 通用视图解决方案ListView 无需再views.py实现函数
    # 以下两种方法相同，仅仅写法不同
    (r'^publishers/$', publisherinfo),
    (r'^publishers/$', ListView.as_view(    
            queryset=Publisher.objects.all(),
            context_object_name='publisherlist',
            template_name='publisher_list_page.html')),    
    #********************************************************************#
)
#**************************通用视图解决方案******************************# 

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^debuginfo/$', views.test),
    )
urlpatterns += patterns('MyDJ.views',  
    (r'^', 'test'),    
)
urlpatterns += staticfiles_urlpatterns()
