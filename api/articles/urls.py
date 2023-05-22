from django.urls import path

from . import views

urlpatterns = [
    path("", views.fetch_articles),
    path("create/<int:id>/", views.create_article),
    path("test/", views.test),
    # path("sample/", UserViewSet.as_view({'get': 'list'}))
]
