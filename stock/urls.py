# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views_auth import CustomAuthToken, Logout

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'stock-items', StockItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('api/logout/', Logout.as_view(), name='api_logout'),
    path('api/download-shop-items/<int:shop_id>/', download_shop_items, name='download_shop_items'),
]