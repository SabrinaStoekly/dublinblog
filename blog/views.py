from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm, PostForm, UpdatePostForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils.decorators import method_decorator


class LastThreePosts(generic.ListView):
    model = Post
    queryset = Post.objects.order_by("-created_on")[:3]
    template_name = "index.html"
    context_object_name = "last_three_posts"


class ViewAllPosts(generic.ListView):
    model = Post
    queryset = Post.objects.order_by("-created_on")
    template_name = "all_posts.html"
    paginate_by = 6
    context_object_name = "view_all_posts"


class PostDetail(View):
    template_name = "post_detail.html"

    def get_post_details(self, slug):
        return get_object_or_404(Post, slug=slug)

    def get_context_data(self, **kwargs):
        post = kwargs['post']
        liked = post.likes.filter(id=self.request.user.id).exists()
        approved_comments = kwargs.get('approved_comments', None)
        commented = kwargs.get('commented', False)

        context = {
            "post": post,
            "comments": approved_comments,
            "liked": liked,
            "commented": commented,
            "comment_form": CommentForm(),
        }

        return context

    def get(self, request, slug, *args, **kwargs):
        post = self.get_post_details(slug)
        approved_comments = post.comments.filter(approved=True)
        context = self.get_context_data(post=post, approved_comments=approved_comments)
        return render(request, self.template_name, context)

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.author = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )
      


# View to add a post
@method_decorator(login_required, name='dispatch')
class AddPost(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    slug_field = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created!')
        return super().form_valid(form)


# View to update a post
class UpdatePost(View):
    template_name = 'update_post.html'

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            "post": post,
            "comments": comments,
            "liked": liked,
            "comment_form": CommentForm(),
            "form": UpdatePostForm(instance=post),
        }

        return render(request, self.template_name, context)

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        form = UpdatePostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", slug=slug)
        
        context = {
            "post": post,
            "comment_form": CommentForm(),
            "form": form,
        }

        return render(request, self.template_name, context)


# View to delete a post
class DeletePost(generic.DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
    success_message = 'Post deleted successfully'

    def test_func(self):
        # Check if the current user is the author of the post
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeletePost, self).delete(request, *args, **kwargs)


class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))

