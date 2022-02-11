from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'threads', views.ThreadViewSet)
#router.register(r'myview', views.PiecesAPIView.as_view(),basename="myview")    

urlpatterns = [
    path('', include(router.urls)),
    path('verify_chats/', views.verify_chats),
]

#urlpatterns = format_suffix_patterns(urlpatterns)