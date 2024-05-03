from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Question, Tag, Comment
from .forms import CommentForm, SignUpForm
from django.http import HttpResponseRedirect
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import QuestionSerializer, TagSerializer, CommentSerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login


class QuestionAPIPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = QuestionAPIPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        return super().get_queryset().order_by('-date')[:3]


class AllQuestionsView(ListView):
    template_name = 'blog/all-questions.html'
    model = Question
    context_object_name = 'all_questions'

    def get_queryset(self):
        return super().get_queryset().order_by('-date')


class ReviewDetailView(View):
    def is_stored_question(self, request, question_id):
        stored_questions = request.session.get('stored_questions')
        if stored_questions is not None:
            is_saved_for_later = question_id in stored_questions
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        question = Question.objects.get(slug=slug)

        context = {
            'question': question,
            'question_tags': question.tag.all(),
            'comment_form': CommentForm(),
            'comments': question.comments.all().order_by('-id'),
            'saved_for_later': self.is_stored_question(request, question.id),
        }

        return render(request, 'blog/question-detail.html', context)

    @method_decorator(login_required)
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        question = Question.objects.get(slug=slug)
        user = request.user

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.question = question
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('question-detail-page', args=[slug]))

        context = {
            'question': question,
            'question_tags': question.tag.all(),
            'comment_form': comment_form,
            'comments': question.comments.all().order_by('-id'),
            'saved_for_later': self.is_stored_question(request, question.id),
        }
        return render(request, 'blog/question-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        stored_questions = request.session.get('stored_questions')
        context = {}

        if stored_questions is None or len(stored_questions) == 0:
            context['questions'] = []
            context['has_questions'] = False
        else:
            questions = Question.objects.filter(id__in=stored_questions)
            context['questions'] = questions
            context['has_questions'] = True

        return render(request, 'blog/stored-questions.html', context)

    def post(self, request):
        stored_questions = request.session.get('stored_questions')

        if stored_questions is None:
            stored_questions = []

        question_id = int(request.POST['question_id'])

        if question_id not in stored_questions:
            stored_questions.append(question_id)
        else:
            stored_questions.remove(question_id)

        request.session['stored_questions'] = stored_questions

        return HttpResponseRedirect('/')  # redirect to starting page


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

