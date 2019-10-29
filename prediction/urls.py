from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('prediction', views.Fare_predictionView)

urlpatterns = [
    path('', views.home, name = 'home' ),
    path('add', views.add, name = 'add'),
    path('api/', include(router.urls)),
    path('status/', views.ml_model),
    path('form/', views.pred_form, name = 'cxform'),
]
