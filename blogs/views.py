from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

def news(request):
    posts = Post.objects.all().order_by('-created_at')  # Νεότερα πρώτα
    context = {'posts': posts}
    return render(request, 'news.html', context)

def details(request, pk, author_id):
    post = get_object_or_404(Post, pk=pk)  # Αντικείμενο ή 404
    author = get_object_or_404(User, pk=author_id)

    context = {
        'post': post,  # Δεν χρειάζεται .values(), το object είναι προσβάσιμο στο template
        'username': author.username,
    }
    return render(request, 'details.html', context)
