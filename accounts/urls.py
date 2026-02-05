from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views




app_name = 'accounts'
urlpatterns = [
   
    path('signup/', views.signup , name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('dashboard/' , views.dashboard , name='dashboard'),
]