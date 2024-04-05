
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from .custom_permissions import OnlyLoggedSuperUser
from django.db.models import Q
from hitcount.views import get_hitcount_model, HitCountMixin


from .models import News, Category
from .forms import ContactForm, CommentForm

    

# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'
#     context_object_name = 'news'



def newsdetail(request, news):
    news = get_object_or_404(News, slug=news,status = News.Status.Published)

    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits +=1
        hitcontext["hit_counted"] = hit_count_response.hit_counted 
        hitcontext["hit_message"] = hit_count_response.hit_message 
        hitcontext["total_hits"] = hits 


    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Yangi komment yaratiladi lekn DB saqlanmaydi
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov jonatayotgan foydalanuvchiga bog'lab qo'yamiz
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        "comments": comments,
        "new_comment": new_comment,
        "comment_count": comment_count,
        "comment_form": comment_form,
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




class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status', 'category', )
    template_name = "crud/update.html"




class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = "crud/delete.html"
    success_url =  reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = "crud/create.html"
    fields = ('title', 'slug', 'body', 'image', 'status', 'category', )
    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)


    context = {
        "admin_users": admin_users
    }
    return render(request, 'pages/admin.html', context)




class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get("q")
        return News.objects.all().filter(
            Q(title__icontains =  query) | Q(body__icontains =  query)
        )









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











