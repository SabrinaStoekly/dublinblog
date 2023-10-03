from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

# Database model for blog posts
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Tourist Attraction', 'Tourist Attraction'),
        ('Pubs', 'Pubs'),
        ('Restaurants', 'Restaurants'),
    ]

    title = models.CharField(max_length=250, unique=False)
    slug = models.SlugField(max_length=250, unique=True)    
    category = models.CharField(
        max_length=30,  
        choices=CATEGORY_CHOICES,
        default='Tourist Attraction'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    @property
    def approved_comments_count(self):
        return self.comments.filter(approved=True).count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_on']

# Define a function to generate the slug before saving
@receiver(pre_save, sender=Post)
def generate_post_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + uuid.uuid4().hex.upper())


# Database model for blog comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.CharField(max_length=80)    
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
