from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from contacts import views

urlpatterns = [
    path('', views.ContactList.as_view()),
    path('lookup/<int:pk>/', views.ContactDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)