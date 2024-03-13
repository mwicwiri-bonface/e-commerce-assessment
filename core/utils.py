import io
from random import randint

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


def generate_key(minlength=20, maxlength=20, use_lower=True, use_upper=True, use_numbers=True, use_special=False):
    charset = ''
    if use_lower:
        charset += "abcdefghijklmnopqrstuvwxyz"
    if use_upper:
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        charset += "123456789"
    if use_special:
        charset += "~@#$%^*()_+-={}|]["
    if minlength > maxlength:
        length = randint(maxlength, minlength)
    else:
        length = randint(minlength, maxlength)
    key = ''
    for i in range(0, length):
        key += charset[(randint(0, len(charset) - 1))]
    return key


class TimeStampModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']


# function for converting images to webp
def convert_to_webp(image):
    img = Image.open(image)
    img = img.convert('RGB')
    # img = img.resize((800, 800))
    width, height = img.size
    # Calculate the aspect ratio
    aspect_ratio = width / height
    new_width = 800
    new_height = int(new_width / aspect_ratio)
    # Crop the image
    img = img.resize((new_width, new_height), Image.LANCZOS)
    # # Convert the image to WebP format
    output = io.BytesIO()
    img.save(output, format='webp', quality=60)
    output.seek(0)

    # Update the image field with the converted WebP image
    buffer = InMemoryUploadedFile(
        output, 'ImageField', f"{image.name.split('.')[0]}.webp",
        'image/webp', output.getbuffer().nbytes, None
    )
    return buffer
