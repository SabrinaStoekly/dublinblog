from django.urls import path
from . import views

urlpatterns = [
    path('', views.LastThreePosts.as_view(), name='home'),
    path('view-all-posts/', views.ViewAllPosts.as_view(), name='view_all_posts'),
    path('add_post/', views.AddPost.as_view(), name='add_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/update/<slug:slug>/', views.UpdatePost.as_view(), name='update_post'),
    path('post/delete/<slug:slug>/', views.DeletePost.as_view(), name='delete_post'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),    
]