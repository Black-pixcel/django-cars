from django.contrib import admin
from .models import *

# Register your models here.
for model in [Colors, Brands, Models, Orders]:
    admin.site.register(model)