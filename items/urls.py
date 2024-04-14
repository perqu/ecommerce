from django.urls import path
from .views import ItemsByCategoryView, AllItemsView, AllCategoriesView

urlpatterns = [
    path('/category/<uuid:uuid>/', ItemsByCategoryView.as_view(), name='items_by_category'),
    path('', AllItemsView.as_view(), name='items'),
    path('/categories', AllCategoriesView.as_view(), name='categories'),
]
