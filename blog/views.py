from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from .forms import CommentForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        try:
            context['following'] = user in self.request.user.profile.following.all()
        except: context['following'] = False
        return context

class FeedView(ListView):
    model = Post
    template_name = 'blog/feed.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        qset = Post.objects.filter(author=self.request.user)
        for u in self.request.user.profile.following.all():
            qset |= Post.objects.filter(author=u)
        return qset.order_by('-date_posted')


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(parent=post).order_by("-date_posted")

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            Comment.objects.create(
                parent = post,
                author = request.user,
                content = content
            ).save()
            return redirect(post.get_absolute_url())
    
    else: comment_form = CommentForm()

    context = {
        'comments' : comments,
        'object' : post,
        'comment_form': comment_form
    }

    return render(request, 'blog/post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
