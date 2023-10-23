from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        base_query = super().get_queryset()
        latest_posts = base_query.order_by('-date')[:3]
        return latest_posts


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, "blog/index.html",
#                   {'posts': latest_posts}
#                   )


class PostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name = 'all_posts'

    def get_queryset(self):
        base_query = super().get_queryset()
        latest_posts = base_query.order_by('-date')[:3]
        return latest_posts


# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, "blog/all-posts.html",
#                   {'all_posts': all_posts}
#                   )

class ReviewDetailView(DetailView):
    template_name = 'blog/post-detail.html'
    model = Post

    # def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         loaded_review = self.object
    #         request = self.request
    #         favorite_id = request.session.get("favorite_review")
    #         context["is_favorite"] = favorite_id == str(loaded_review.id)
    #         return context


# def post_detail(request, slug):
#     # identified_post = Post.objects.get(slug=slug)
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html',
#                   {'post': identified_post,
#                    'post_tags': identified_post.tag.all(),
#                    })
