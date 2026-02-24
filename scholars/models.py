from django.db import models
from django.utils.text import slugify
# Create your models here.


class Scholar(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # NEW FIELDS
    short_bio = models.CharField(max_length=300, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    profile_image = models.ImageField(
        upload_to='scholars/', blank=True, null=True)

    birth_year = models.CharField(max_length=50, blank=True)
    death_year = models.CharField(max_length=50, blank=True)
    madhhab = models.CharField(max_length=100, blank=True)
    birth_place = models.CharField(max_length=200, blank=True)

    biography = models.TextField()

    teachers = models.TextField(blank=True)
    students = models.TextField(blank=True)
    famous_books = models.TextField(blank=True)
    notable_quotes = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
