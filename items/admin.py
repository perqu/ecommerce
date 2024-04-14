from django.contrib import admin
from .models import Item, Category, AttributeValue, Attribute

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)