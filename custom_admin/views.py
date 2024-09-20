# custom_admin/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from core.models import Post, Comment, Like
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.db.models.functions import TruncMonth
import csv
from django.http import HttpResponse

# Check if user is an admin
def is_admin(user):
    return user.is_superuser

# Admin Dashboard
def admin_dashboard(request):
    # Bar and Line chart data
    user_count = User.objects.count()
    post_count = Post.objects.count()
    comment_count = Comment.objects.count()
    like_count = Like.objects.count()
    
    # Line chart data for posts over time
    months = ['January', 'February', 'March', 'April', 'May', 'June']  # Example labels
    post_counts = [Post.objects.filter(created_at__month=i).count() for i in range(1, 7)]
    
    # Pie chart data for post distribution by users
    users = User.objects.all()
    user_labels = [user.username for user in users]
    user_post_counts = [user.posts.count() for user in users]
    
    # Doughnut chart data for comment distribution by posts
    posts = Post.objects.all()
    post_labels = [f'Post {post.id}' for post in posts]
    post_comment_counts = [post.comments.count() for post in posts]
    
    context = {
        'user_count': user_count,
        'post_count': post_count,
        'comment_count': comment_count,
        'like_count': like_count,
        'months': months,
        'post_counts': post_counts,
        'user_labels': user_labels,
        'user_post_counts': user_post_counts,
        'post_labels': post_labels,
        'post_comment_counts': post_comment_counts
    }
    
    return render(request, 'custom_admin/dashboard.html', context)

# Manage Users (List, Edit, Delete)
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'custom_admin/manage_users.html', {'users': users})

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('manage_users')
    return render(request, 'custom_admin/edit_user.html', {'user': user})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')

# Manage Posts (List, Delete)
@user_passes_test(is_admin)
def manage_posts(request):
    posts = Post.objects.all()
    return render(request, 'custom_admin/manage_posts.html', {'posts': posts})

@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('manage_posts')

# Manage Comments (List, Delete)
@user_passes_test(is_admin)
def manage_comments(request):
    comments = Comment.objects.all()
    return render(request, 'custom_admin/manage_comments.html', {'comments': comments})

@user_passes_test(is_admin)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('manage_comments')

# Manage Likes (List, Delete)
@user_passes_test(is_admin)
def manage_likes(request):
    likes = Like.objects.all()
    return render(request, 'custom_admin/manage_likes.html', {'likes': likes})

@user_passes_test(is_admin)
def delete_like(request, like_id):
    like = get_object_or_404(Like, id=like_id)
    like.delete()
    return redirect('manage_likes')


# Admin Login
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, "You do not have admin rights.")
    else:
        form = AuthenticationForm()
    return render(request, 'custom_admin/admin_login.html', {'form': form})

# Admin Logout
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@user_passes_test(is_admin)
def report_page(request):
    # Fetch user data
    users = User.objects.all()
    
    # Fetch post data
    posts = Post.objects.all()

    # Monthly post count
    posts_per_month = Post.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    months = [post['month'].strftime('%B %Y') for post in posts_per_month]
    post_counts = [post['count'] for post in posts_per_month]

    context = {
        'users': users,
        'posts': posts,
        'months': months,
        'post_counts': post_counts
    }
    
    return render(request, 'custom_admin/report.html', context)

def download_user_report_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_report.csv"'

    writer = csv.writer(response)
    # Write the header
    writer.writerow(['User ID', 'Username', 'Email', 'Date Joined'])

    # Fetch user data and write rows
    users = User.objects.all().values_list('id', 'username', 'email', 'date_joined')
    for user in users:
        writer.writerow(user)

    return response

def download_post_report_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="post_report.csv"'

    writer = csv.writer(response)
    # Write the header
    writer.writerow(['Post ID', 'Content', 'Author', 'Date Created'])

    # Fetch post data and write rows
    posts = Post.objects.all().values_list('id', 'content', 'user__username', 'created_at')
    for post in posts:
        writer.writerow(post)

    return response