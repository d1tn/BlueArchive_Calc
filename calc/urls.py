from django.urls import path
from . import views

app = 'first_app'
urlpatterns = [
    path('', views.charchoise, name='charchoise'),
    path('input', views.input, name='input'),
    path('calc', views.calc, name='calc'),
    path('saveData', views.saveData, name='saveData'),
    path('loadData', views.loadData, name='loadData'),
    path('howto', views.howto, name='howto'),
    path('about', views.about, name='about'),
    path('privacypolicy', views.privacypolicy, name='privacypolicy'),

    # path('calc', views.calc, name='calc'),
]
