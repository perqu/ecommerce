from rest_framework import serializers
from .models import Category, Attribute, Item, AttributeValue

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['uuid', 'name', 'parent_category', 'subcategories']
        read_only_fields = ['uuid']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['uuid', 'name', 'category']
        read_only_fields = ['uuid']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['uuid', 'name', 'description', 'price', 'category']
        read_only_fields = ['uuid']

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['uuid', 'item', 'attribute', 'value']
        read_only_fields = ['uuid']
