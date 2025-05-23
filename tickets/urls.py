from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('<str:ticket_id>/complete/', views.mark_completed, name='mark_completed'),
    path('<str:ticket_id>/approve/', views.approve_ticket, name='approve_ticket'),
]
