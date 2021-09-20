from django.urls import path
from . import views

app = 'first_app'
urlpatterns = [
    path('', views.charchoise, name='charchoise'),
    path('input', views.input, name='input'),
    path('calc', views.calc, name='calc'),
    path('del', views.delSession, name='del'),
    path('howto', views.howto, name='howto'),
    path('about', views.about, name='about'),

    # path('calc', views.calc, name='calc'),
]
