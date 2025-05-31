from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/my_workouts/', views.MyWorkoutsView.as_view(), name='my_workouts'),
    path('profile/my_subscriptions/', views.MySubscriptionsView.as_view(), name='my_subscriptions'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('full_schedule/', views.FullScheduleView.as_view(), name='full_schedule'),
]
