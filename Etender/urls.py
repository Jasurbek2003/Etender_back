from django.contrib import admin
from django.urls import path

from etenderuzex.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('etenderuzex/category/', CategoryAPIView.as_view()),
    path('etenderuzex/product/', ProductAPIView.as_view()),
    path('etenderuzex/tender/', TenderAPIView.as_view()),
    path('etenderuzex/check/', CheckedTenderAPIView.as_view()),
    path('etenderuzex/user/', TelegramUserAPIView.as_view()),
]
