from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Post, Tag, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect

from .serializers import PostSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return super().get_queryset().order_by('-date')[:3]


class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name = 'all_posts'

    def get_queryset(self):
        return super().get_queryset().order_by('-date')


class ReviewDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),
            'saved_for_later': self.is_stored_post(request, post.id),
        }

        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))

        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),
            'saved_for_later': self.is_stored_post(request, post.id),
        }
        return render(request, 'blog/post-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'blog/stored-posts.html', context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST['post_id'])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect('/')  # redirect to starting page
