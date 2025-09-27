from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib import messages
import random
import re
from home.models import Blog

# Home page
def index(request):
    blogs = Blog.objects.all()
    random_blogs = random.sample(list(blogs), min(len(blogs), 3))
    return render(request, 'index.html', {'random_blogs': random_blogs})

# About page
def about(request):
    return render(request, 'about.html')

# Contact page
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')
        invalid_input = ['', ' ']
        if name in invalid_input or email in invalid_input or phone in invalid_input or message_text in invalid_input:
            messages.error(request, 'One or more fields are empty!')
        else:
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            phone_pattern = re.compile(r'^[0-9]{10}$')

            if email_pattern.match(email) and phone_pattern.match(phone):
                message_body = f'''
From: {name}
Message: {message_text}
Email: {email}
Phone: {phone}
'''
                send_mail('You got a mail!', message_body, '', ['dev.ash.py@gmail.com'])
                messages.success(request, 'Your message was sent.')
            else:
                messages.error(request, 'Email or Phone is Invalid!')

    return render(request, 'contact.html')

# Projects page
def projects(request):
    return render(request, 'projects.html')

# Blog page
def blog(request):
    blogs = Blog.objects.all().order_by('-time')
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'blog.html', {'blogs': blogs})

# Blog post detail
def blogpost(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blogpost.html', {'blog': blog})

# Categories list
def categories(request):
    all_categories = Blog.objects.values('category').distinct().order_by('category')
    return render(request, "categories.html", {'all_categories': all_categories})

# Category page
def category(request, category):
    category_posts = Blog.objects.filter(category=category).order_by('-time')
    paginator = Paginator(category_posts, 3)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    if not category_posts:
        message = f"No posts found in category: '{category}'"
        return render(request, "category.html", {"message": message})
    return render(request, "category.html", {"category": category, 'category_posts': category_posts})

# Search
def search(request):
    query = request.GET.get('q')
    results = Blog.objects.none()
    if query:
        for word in query.split():
            results |= Blog.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    message = "" if results else "Sorry, no results found for your search query."
    return render(request, 'search.html', {'results': results, 'query': query, 'message': message})

# Thanks page
def thanks(request):
    return render(request, 'thanks.html')

# Certifications page
def certifications(request):
    certificates = [
        {"name": "AWS Cloud Security", "issuer": "LetsDefend"},
    {"name": "AWS Certified Cloud Practitioner", "issuer": "A Cloud Guru | A Pluralsight Company"},
    {"name": "Cisco Certified Network Associate (CCNA)", "issuer": "Cisco"},
        {"name": "Cisco Endpoint Security", "issuer": "Cisco Networking Academy"},
        {"name": "Linux Foundation Certified System Administrator (LFCS)", "issuer": "KodeKloud"},
    ]
    return render(request, "certifications.html", {"certificates": certificates})
