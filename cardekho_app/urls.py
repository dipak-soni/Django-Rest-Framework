from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('showroom',ShowRoomViewSet2,basename='showroom')

urlpatterns = [
    path('display/',CarListView,name="car"),
    path('<int:pk>',CarDetailView,name='car_detail'),   
    # path('showroom/',ShowRoomListView.as_view(),name="showroom"),   
    # path('showroom/<int:pk>',ShowRoomDetailView.as_view(),name='showroom_detail'),
    path('',include(router.urls)),
    path('review/',ReviewListView.as_view(),name='review_list'),
    path('review/<int:pk>',ReviewDetailView.as_view(),name='review_detail'),
    # view reviews of car
    path('showroom/<int:pk>/view-review',ViewReviews.as_view()),
    path('showroom/<int:pk>/create-review',CreateReviews.as_view()),
    # path('showroom/review/<int:pk>',ReviewDetail.as_view()),
]
