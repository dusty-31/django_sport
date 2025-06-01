from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('list', views.BlogView.as_view(), name='blog'),
    path('post/<slug:slug>/', views.BlogPostView.as_view(), name='blog_post'),
    path('category/<slug:slug>/', views.BlogCategoryView.as_view(), name='blog_category'),
    path('tag/<slug:slug>/', views.BlogTagView.as_view(), name='blog_tag'),
]
