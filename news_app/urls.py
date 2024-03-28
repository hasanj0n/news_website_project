from django.urls import path
# from .views import newslistview, newsdetail
from .views import newsdetail, HomePageView, page404view, ContactPageView, \
    LocalNewsView, ForeignNewsView, TechnologyNewsView, SportNewsView


# urlpatterns = [
#     path('all/', newslistview, name='news'),
#     path('<int:id>/', newsdetail, name='news_detail'),
# ]


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/<slug:news>/', newsdetail, name='news_detail'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('page404/', page404view, name='page404'),
    path('local/', LocalNewsView.as_view(), name='local'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign'),
    path('sport/', SportNewsView.as_view(), name='sport'),
    path('technology/', TechnologyNewsView.as_view(), name='technology'),
]
