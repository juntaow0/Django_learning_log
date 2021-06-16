"""define urls for users app"""

from django.urls import path, include

app_name="users"
urlpatterns=[
    # default url
    path('',include('django.contrib.auth.urls'))

]