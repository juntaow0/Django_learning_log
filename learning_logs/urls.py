"""learning_logs URL Configuration"""

from django.urls import path
from . import views

app_name ='learning_logs'

urlpatterns = [
    # Home page
    path('',views.index, name='index'),

    # Page of topics
    path('topics',views.topics,name='topics'),

    # details of each topic
    path('topics/<int:topic_id>/', views.topic, name='topic')
]
