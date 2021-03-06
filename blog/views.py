from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth.models import User
from .models import Comment
from .forms import CommentForm
from django.urls import reverse_lazy, reverse


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class SelfPostListView(ListView):
    model = Post
    template_name = 'blog/self_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView,LoginRequiredMixin):
    model = Post


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
    success_url = '/main'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def home (request):
    return render(request, 'blog/landing.html')

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def search_user(request):
    if request.method =="POST":
        searched = request.POST['searched']
        users=User.objects.filter(username__contains=searched)
        posts=Post.objects.filter(title__contains=searched)
        return render(request, 'blog/search-results.html',{'searched':searched,
                                                            'users':users,
                                                            'posts':posts})
    else:
        return render(request, 'blog/search-results.html',{})

class AddCommentView(LoginRequiredMixin,CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'blog/add_comment.html'
	#fields = '__all__'
	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)

	success_url = reverse_lazy('blog-home')