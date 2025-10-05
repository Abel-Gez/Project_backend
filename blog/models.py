from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publishDate = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)

    # Save uploaded images to static/uploads/
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
