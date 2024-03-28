from .models import News, Category

def latest_news(request):
    latest_news = News.published.all().order_by('-published_time')[:10]
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'latest_news': latest_news,
    }

    return context