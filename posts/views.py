from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.contenttypes.models import ContentType

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch comments using Generic Relation
        context['comments'] = self.object.comments.all()
        print("comments",self.object.comments.all())
        return context


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_form.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_form.html'


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/post_confirm_delete.html'


class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'posts/post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(
                self.model)
            comment.object_id = self.object.id
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
