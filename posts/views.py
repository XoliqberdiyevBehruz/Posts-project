from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from hitcount.views import HitCountDetailView, HitCountMixin
from posts.forms import PostCommentForm
from .models import Post, PostComment
from django.views import View
from django.views.generic import CreateView
from hitcount.utils import get_hitcount_model


class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(published=True)

        return render(request, 'posts/post_list.html', {'posts':posts})
    
class PostDetailView(HitCountDetailView):

    def get(self, request, id):
        post = Post.objects.filter(published=True)
        post = post.get(id=id)
        comment_form = PostCommentForm()
        context = {}
        hit_count = get_hitcount_model().objects.get_for_object(post)
        hits = hit_count.hits
        context['hitcount'] = {'pk': hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        if hit_count_response.hit_counted:
                    hits = hits + 1
                    context['hitcount']['hit_counted'] = hit_count_response.hit_counted
                    context['hitcount']['hit_message'] = hit_count_response.hit_message
                    context['hitcount']['total_hits'] = hits


        return render(request, 'posts/post_detail.html', {'post':post, 'comment_form':comment_form})
    
    def post(self, request, id):
        post = Post.objects.filter(published=True)
        post = post.get(id=id)
        comment_form = PostCommentForm(data=request.POST)
        context = {
            'comment_form':comment_form
        }
        if comment_form.is_valid():
            PostComment.objects.create(
                post=post,
                author=request.user,
                comment=comment_form.cleaned_data['comment']
            )

            return redirect('posts:detail', kwargs={'id':post.id})
        else:
            return render(request, 'posts/post_detail.html', context)

class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ('title','description','photo')
    success_url = reverse_lazy('posts:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



    

 