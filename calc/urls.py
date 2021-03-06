from django.urls import path
from . import views

handler500 = views.my_customized_server_error

app = 'calc'
urlpatterns = [
    path('', views.charchoise, name='charchoise'),
    path('input', views.input, name='input'),
    path('result', views.result, name='result'),
    path('saveConfirm', views.saveConfirm, name='saveConfirm'),
    path('saved', views.saved, name='saved'),    path('loadData', views.loadData, name='loadData'),
    path('loaded', views.loaded, name='loaded'),
    path('howto', views.howto, name='howto'),
    path('about', views.about, name='about'),
    path('privacypolicy', views.privacypolicy, name='privacypolicy'),
    path('deleteSession', views.deleteSession, name='deleteSession'),
    path('ads.txt', views.ads, name='ads'),
]
