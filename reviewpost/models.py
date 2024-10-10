from pathlib import Path
import requests
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import environ
from vercel_storage import blob

class ReviewModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    useful_num = models.IntegerField(null=True, blank=True, default=0)
    product_image = models.ImageField(upload_to='reviews/images/', null=True, blank=True)
    product_image_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Save the image if it exists
        if self.product_image:
            resp = blob.put(
                pathname=self.product_image.name,
                body=self.product_image,
                options={'token': settings.VERCEL_BLOB_TOKEN}
            )

            # Clear the local image field
            self.product_image = None

            # Save the URL of the uploaded image
            self.product_image_url = resp['url']

        # Perform the usual save operation
        super().save(*args, **kwargs)