from django.urls import path, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from snippets.views import UserViewSet, SnippetViewSet
from rest_framework.routers import DefaultRouter


"""urlpatterns=[
    path("snippets/", views.snippet_list),
    path("snippets/<int:pk>/", views.snippet_detail),
]
"""

"""
snippet_list=SnippetViewSet.as_view({
    "get":"list",
    "post":"create"
})
snippet_detail=SnippetViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
})
snippet_highlight=SnippetViewSet.as_view({
    'get':'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list=UserViewSet.as_view({
    'get':'list'
})
user_detail=UserViewSet.as_view({
    'get':'retrieve'
})

urlpatterns=[
    path("snippets/", snippet_list, name="snippet-list"),
    path("snippets/<int:pk>/", snippet_detail, name="snippet-detail"),
    path("snippet/<int:pk>/highlight/", snippet_highlight, name="snippet-highlight"),
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>", user_detail, name="user-detail"),
]
urlpatterns=format_suffix_patterns(urlpatterns)
"""

#using router for automated url routing

router=DefaultRouter()
router.register(r"snippets", views.SnippetViewSet, basename="snippet")
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns=[
    path("", include(router.urls))
]