from datetime import date
from django.shortcuts import render
from .models import Post


def starting_page(request):
    all_posts = Post.objects.all()
    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_posts = sorted_posts[-3:]
    return render(request, "blog/index.html",
                  {'posts': all_posts}
                  )


def posts(request):
    all_posts = Post.objects.all()
    return render(request, "blog/all-posts.html",
                  {'all_posts': all_posts}
                  )


def post_detail(request, slug):
    identified_post = Post.objects.get(slug=slug)
    return render(request, 'blog/post-detail.html',
                  {'post': identified_post})
