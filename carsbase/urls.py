from django.urls import path, include
from rest_framework import routers
from . import views
from .yasg import urlpatterns as swagger_urls
# from .api import OrdersViewSet


router = routers.DefaultRouter()
router.register('colors', views.ColorsViewSet, basename='colors')
router.register('brands', views.BrandsViewSet, basename='brands')
router.register('models', views.ModelsViewSet, basename='models')
router.register('orders', views.OrdersViewSet, basename='orders')


urlpatterns = [
    path('', views.OrdersViewFull.as_view(), name='base'),
    path('filter/', views.OrdersViewFull.as_view(), name='filter'),
    path('api/v1/', include(router.urls))
]

urlpatterns += swagger_urls
