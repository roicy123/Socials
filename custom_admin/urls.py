from django.urls import path
from custom_admin import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('posts/', views.manage_posts, name='manage_posts'),
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comments/', views.manage_comments, name='manage_comments'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('likes/', views.manage_likes, name='manage_likes'),
    path('likes/delete/<int:like_id>/', views.delete_like, name='delete_like'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('report/', views.report_page, name='admin_reports'),
    path('download_user_report_csv/', views.download_user_report_csv, name='download_user_report_csv'),
    path('download_post_report_csv/', views.download_post_report_csv, name='download_post_report_csv'),
]
