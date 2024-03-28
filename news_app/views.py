from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import News, Category
from .forms import ContactForm
from django.http import HttpResponse




    

# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'
#     context_object_name = 'news'

def newsdetail(request, news):
    news = get_object_or_404(News, slug=news,status = News.Status.Published)
    context = {
        "news": news
    }
    return render(request=request, template_name='news/news_detail.html', context=context)




# Home page view
    
class HomePageView(ListView):
    template_name = 'news/index.html'
    model = News  # Define the model for the ListView

    def get_queryset(self):
        # Return the queryset you want to use for the ListView
        return News.published.all().order_by('-published_time')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['local_news_list'] = News.published.filter(category__name='Mahalliy')[:5]
        context['foreign_news'] = News.published.filter(category__name='Xorij')[:5]
        context['sport_news'] = News.published.filter(category__name='Sport')[:5]
        context['technology_news'] = News.published.filter(category__name='Texnologiya')[:5]
        return context




# def homepageview(request):
#     news = News.published.all().order_by('-published_time')[:5]
#     categories = Category.objects.all()
#     local_one = News.published.all().filter(category__name = 'Mahalliy')[:1 ]
#     local_news = News.published.all().filter(category__name = 'Mahalliy')[1:6]
#     context = {
#         'news_list': news,
#         'categories': categories,
#         'local_news_ones': local_one,
#         'local_news_list': local_news,
#     }
#     return render(request=request, template_name='news/index.html', context=context, )








# Contact page view
class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form" : form
        }
        return render(request=request, template_name='news/contact.html', context=context)
    

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Thank you for your meassage.</h2>")
        context = {
            "form" : form
        }
        return render(request=request, template_name='news/contact.html', context=context)





# Page404 view
def page404view(request):
    context = {
    
    }
    return render(request=request, template_name='news/404.html', context=context)






class LocalNewsView(ListView):
    model = News
    template_name = 'news/local.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        return News.published.all().filter(category__name = "Mahalliy")



class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign.html'
    context_object_name = 'foreign_news'

    def get_queryset(self):
        return News.published.all().filter(category__name='Xorij')


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology.html'
    context_object_name = 'technology_news'
    
    def get_queryset(self):
        return News.published.all().filter(category__name='Texnologiya')



class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        return News.published.all().filter(category__name='Sport')























# def contactpageview(request):
#     print(request.POST)
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Thank you for Contact us!")
#     context = {
#         "form" : form
#     }
    
#     return render(request=request, template_name='news/contact.html', context=context)









# def newslistview(request):
#     news_list = News.published.all()
#     # news_list = News.objects.filter(status = News.Status.Published).all()
#     context = {
#         'news_list': news_list
#     }

#     return render(request=request, template_name='news/news.html', context=context)





# def newsdetail(request, id):
#     news = get_object_or_404(News, id=id,status = News.Status.Published)
#     context = {
#         "news": news
#     }
#     return render(request=request, template_name='news/news_detail.html', context=context)











