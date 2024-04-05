from django.urls import path
# from .views import newslistview, newsdetail
from .views import newsdetail, HomePageView, page404view, ContactPageView, \
    LocalNewsView, ForeignNewsView, TechnologyNewsView, SportNewsView, NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_view, SearchResultsList


# urlpatterns = [
#     path('all/', newslistview, name='news'),
#     path('<int:id>/', newsdetail, name='news_detail'),
# ]


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/<slug:news>/', newsdetail, name='news_detail'),
    path('news/create', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug>/update', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('page404/', page404view, name='page404'),
    path('local/', LocalNewsView.as_view(), name='local'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign'),
    path('sport/', SportNewsView.as_view(), name='sport'),
    path('technology/', TechnologyNewsView.as_view(), name='technology'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name="search_result"),

]
