from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Cause)
admin.site.register(Donation)
admin.site.register(TeamMember)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(CategoryImage)
# admin.site.register(GalleryImage)