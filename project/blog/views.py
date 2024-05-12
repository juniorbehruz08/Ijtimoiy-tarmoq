import operator
import random
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import *
from .forms import ArticleForm, LoginForm, RegistrationForm, CommentForm, MessageForm, PhotoForm, GroupMessageForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q


# Create your views here.

def index(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('HomePage')
            else:
                return redirect('index')
        else:
            return redirect('index')
    else:
        form = LoginForm()

        context = {
            'form': form,
            'title': 'Login'
        }

        return render(request, "user_login.html", context)


def HomePage(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    articles = []
    last_three = Article.objects.all().order_by('-created_date')[:3]
    four_to_seven = Article.objects.all().order_by('-created_date')[3:7]
    most_viewed_5 = Article.objects.filter(created_date__range=(start_date, end_date)).order_by('-views')[:5]
    article = Article.objects.all()
    liked_article = []
    if request.user.is_authenticated:
        liked = Liked.objects.filter(user=request.user)
        for i in liked:
            liked_article.append(i.article)
    adv = Advertisement.objects.all()
    a = request.GET.get('muammo')
    if a and request.user.is_authenticated:
        a = Problem.objects.create(user=request.user, problem=str(a))
        a.save()
    while True:
        if len(articles) == 8 or len(articles) == len(article):
            break
        else:
            a = random.randint(0, len(article) - 1)
            if article[a] not in articles:
                articles.append(article[a])
            else:
                continue

    article1 = Article.objects.all().order_by('-created_date')[0]
    categories = Category.objects.all()
    context = {
        'article1': article1,
        'last_three': last_three,
        'title': 'HomePage',
        'four_to_seven': four_to_seven,
        'most_viewed_5': most_viewed_5,
        'articles': articles,
        'categories': categories,
        'total': len(Article.objects.all()),
        'liked_article': liked_article,
        'adv': adv[:5]
    }

    return render(request, "index.html", context)


def exit(request):
    context = {
        'title': 'EXIT'
    }
    action = request.GET.get('action')
    if action:
        if action == 'yes':
            logout(request)
            return redirect('index')
        else:
            return redirect('HomePage')
    else:
        return render(request, 'yes_or_not.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        try:
            User.objects.get_by_natural_key(form.username)
            return redirect('register')
        except:
            if form.is_valid():
                form.save()
                return redirect('index')
            else:
                return redirect('register')
    else:
        form = RegistrationForm()
        context = {
            'form': form,
            'title': 'Register',
            'text': "Registratsiyadan o'tganingizdan so'ng login qilib kirishingiz lozim!!!"
        }
        return render(request, 'register.html', context)


def add_article(request):
    from datetime import datetime

    current_date = datetime.now()
    formatted_date = current_date.strftime("%d.%m.%Y")
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            slug = f'{str(formatted_date)}_{article.title}_{article.user.username}'
            article.slug = slugify(slug)
            article.save()
            return redirect('HomePage')

    else:
        form = ArticleForm

    context = {
        'form': form,
        'title': 'ADD ARTICLE'
    }

    return render(request, 'add_article.html', context)


def category(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'title': 'CATEGORY'
    }

    return render(request, 'category_page.html', context)


def category_page(request, slug):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    articles = []
    category = Category.objects.get(slug=slug)
    article = Article.objects.filter(category=category)
    categories = Category.objects.all()
    most_viewed_5 = Article.objects.filter(category__slug=slug, created_date__range=(start_date, end_date)).order_by('-views')[:5]
    liked = Liked.objects.filter(user=request.user)
    liked_article = []
    adv = Advertisement.objects.all()
    a = request.GET.get('muammo')
    if a:
        a = Problem.objects.create(user=request.user, problem=str(a))
        a.save()
    for i in liked:
        liked_article.append(i.article)
    while True:
        if len(article) == 8 or len(articles) == len(article):
            break
        else:
            a = random.randint(0, len(article) - 1)
            b = article[a]
            if b not in articles:
                articles.append(b)
            else:
                continue
    context = {
        'articles': articles,
        'title': f'CATEGORY: {category.title.upper()}',
        'category': category,
        'categories': categories,
        'most_viewed_5': most_viewed_5,
        'liked_article': liked_article,
        'adv': adv[:5]
    }
    return render(request, 'category_page_articles.html', context)


def article_detail(request, slug):
    articles = []
    article = Article.objects.get(slug=slug)
    categories = Category.objects.all()
    articless = Article.objects.all()
    comments = article.comments.all().order_by('-date')[:10]
    a = request.GET.get('muammo')
    adv = Advertisement.objects.all()
    if a:
        a = Problem.objects.create(user=request.user, problem=str(a))
        a.save()
    while True:
        if len(articles) == 5 or len(articles) == len(articless):
            break
        else:
            a = random.randint(0, len(articless) - 1)
            b = articless[a]
            if b not in articles:
                articles.append(b)
            else:
                continue

    article.views += 1
    article.save()
    try:
        Liked.objects.get(user=request.user, article=article)
        color = 'black'
    except:
        color = 'white'
    context = {
        'article': article,
        'title': f'{article.title.upper()}',
        'categories': categories,
        'articles': articles,
        'carousel': articles[:3],
        'form': CommentForm(),
        'comments': comments,
        'color': f'{color}',
        'adv': adv[:5]
    }

    return render(request, 'article_detail.html', context)


def save_comment(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.article = Article.objects.get(pk=article_pk)
        comment.save()

    return redirect('article_detail', article.slug)


def search(request):
    word = request.GET.get('search')
    if word:
        article = Article.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        articles = []
        while True:
            if len(articles) == 8 or len(articles) == len(article):
                break
            else:
                a = random.randint(0, len(article) - 1)
                if article[a] not in articles:
                    articles.append(article[a])
                else:
                    continue

        most_viewed_5 = article.order_by("-views")[:5]

        context = {
            'title': f'Search = {word}',
            'articles': articles,
            'total': len(article),
            'categories': Category.objects.all(),
            'most_viewed_5': most_viewed_5
        }

        return render(request, 'search.html', context)
    else:
        return redirect('HomePage')


def chat(request):
    chattes = []
    user = request.user
    chats = Chat.objects.filter(user1=user)
    chat = Chat.objects.filter(user2=user)

    for i in chats:
        chattes.insert(0, i)
    for i in chat:
        chattes.insert(0, i)

    context = {
        'title': 'CHATS',
        'chats': chattes,
    }

    return render(request, 'chat.html', context)


def message(request, chat_slug):
    you = []
    chats = Chat.objects.get(slug=chat_slug)
    messages = chats.messages.all()[:200]
    user1_message = chats.messages.filter(user=request.user)
    for i in messages:
        if i not in user1_message:
            you.append(i)
    title = 'CHAT'
    context = {
        'title': title,
        'you': you,
        'own_message': user1_message,
        'chat': chats,
        'form': MessageForm(),
        'messages': messages,
        'chats': chats
    }

    return render(request, 'message.html', context)


def save_message(request, slug):
    print(request.POST)
    print(request.FILES)
    chat = Chat.objects.get(slug=slug)
    if request.method == 'POST':
        if request.FILES.get('photo') and request.POST.get('message'):
            photo = request.FILES.get('photo')
            data = Message.objects.create(user=request.user, message=request.POST['message'], chat=chat, photo=photo)
            data.save()
        elif request.FILES.get('photo'):
            data = Message.objects.create(user=request.user, photo=request.FILES['photo'], chat=chat)
            data.save()
        elif request.POST.get('message'):
            data = Message.objects.create(user=request.user, message=request.POST['message'], chat=chat)
            data.save()

        return redirect('message', chat.slug)


def add_chat(request):
    users = []
    user = User.objects.all()
    for i in user:
        if i != request.user:
            users.append(i)
    user2 = request.GET.get('user')
    if user2:
        user_2 = User.objects.get(username=user2)
        a = Chat(user1=request.user, user2=user_2, slug=slugify(str(request.user.username) + str(user2)))
        b = len(Chat.objects.filter(user1=request.user, user2=user_2,
                                    slug=slugify(str(request.user.username) + str(user2))))
        c = len(Chat.objects.filter(user1=user_2, user2=request.user,
                                    slug=slugify(str(user2) + str(request.user.username))))
        if c == 0 and b == 0:
            a.save()
            return redirect('message', slugify(str(request.user.username) + str(user2)))
        else:
            if c == 1:
                return redirect('message', slugify(str(user2) + str(request.user.username)))
            elif b == 1:
                return redirect('message', slugify(str(request.user.username) + str(user2)))
            else:
                return redirect('chat')
    search_result = request.GET.get('search')
    if search_result:
        result = User.objects.filter(
            Q(username__icontains=search_result)
        )
        users.clear()
        for i in result:
            if i != request.user:
                users.append(i)

    context = {
        'title': 'ADD CHAT',
        'users': users
    }

    return render(request, 'add_chat.html', context)


def profile(request):
    sort = request.GET.get('sort')
    image = []
    views = []
    if sort:
        article = Article.objects.filter(user=request.user).order_by(sort)
    else:
        article = Article.objects.filter(user=request.user).order_by('-created_date')
    a = AccountPhoto.objects.filter(user=request.user)
    total_article = len(Article.objects.filter(user=request.user))
    b = Article.objects.filter(user=request.user)
    for i in b:
        views.append(i.views)

    total_views = sum(views)

    liked = Liked.objects.filter(user=request.user)
    liked_article = []
    for i in liked:
        liked_article.append(i.article)

    for i in a:
        image.append(i.photo.url)
        break
    if image:
        photo = image[0]
    else:
        photo = 'https://alumni.tcnj.edu/wp-content/uploads/sites/16/2022/06/user-icon-placeholder.png'

    context = {
        'title': 'Profile',
        'articles': article,
        'most_viewed': article.order_by('-views'),
        'image': photo,
        'total_article': total_article,
        'total_views': total_views,
        'liked_article': liked_article
    }

    return render(request, 'profile.html', context)


def save_photo(request):
    if request.method == 'POST':
        form = PhotoForm(files=request.FILES)
        if AccountPhoto.objects.filter(user=request.user):
            a = AccountPhoto.objects.get(user=request.user)
            a.delete()
        if form.is_valid():
            salom = form.save(commit=False)
            salom.user = request.user
            salom.save()
            return redirect('profile')
        else:
            return redirect('profile')

    context = {
        'form': PhotoForm(request.FILES, request.POST),
        'title': 'ADD PHOTO'
    }

    return render(request, 'add_photo.html', context)


def view_account(request, username):
    views = []
    user = User.objects.get(username=username)
    sort = request.GET.get('sort')
    if sort:
        articles = Article.objects.filter(user=user).order_by(sort)
    else:
        articles = Article.objects.filter(user=user)
    image = []
    photo = AccountPhoto.objects.filter(user=user)
    total_article = len(articles)
    for i in articles:
        views.append(i.views)
    if photo:
        for i in photo:
            image.append(i.photo.url)
            break
    else:
        image.append('https://alumni.tcnj.edu/wp-content/uploads/sites/16/2022/06/user-icon-placeholder.png')
    liked_article = []
    if request.user.is_authenticated:
        liked = Liked.objects.filter(user=request.user)
        for i in liked:
            liked_article.append(i.article)

    context = {
        'articles': articles,
        'image': image[0],
        'title': f'Profile {username}',
        'user': user,
        'total_article': total_article,
        'total_views': sum(views),
        'liked_article': liked_article
    }
    return render(request, 'view_account.html', context)


def save_chat(request, username):
    user_2 = User.objects.get(username=username)

    try:
        try:
            Chat.objects.get(user1=request.user, user2=user_2, slug=slugify(str(request.user.username) + str(username)))
            return redirect('message', slugify(str(request.user.username) + str(username)))
        except:
            Chat.objects.get(user1=user_2, user2=request.user, slug=slugify(str(username) + str(request.user.username)))
            return redirect('message', slugify(str(username) + str(request.user.username)))
    except:
        chat = Chat(user1=request.user, user2=user_2, slug=slugify(str(request.user.username) + str(username)))
        chat.save()
        return redirect('message', slugify(str(request.user.username) + str(username)))


def delete_chat(request, chat_slug):
    action = request.GET.get('action')
    if action:
        chats = Chat.objects.get(slug=chat_slug)
        if action == 'yes':
            chats.delete()
            return redirect('chat')
        else:
            return redirect('chat')
    else:
        return render(request, 'yes_or_not.html', {'title': 'DELETE | CHAT'})


def delete_article(request, article_slug):
    article = Article.objects.get(slug=article_slug)

    action = request.GET.get('action')
    if action:
        if action == 'yes':
            share = Saved.objects.filter(url=article_slug)
            for i in share:
                i.is_share = False
                i.url = ''
                i.image = ''
                i.save()
            messages = Message.objects.filter(url=article_slug)
            for i in messages:
                i.is_share = False
                i.url = ''
                i.image = ''
                i.save()
            article.delete()
            return redirect('profile')
        else:
            return redirect('profile')
    else:
        return render(request, 'yes_or_not.html', {'title': 'DELETE | ARTICLE'})


def ranking(request):
    rank = {}
    index = 1
    for i in User.objects.all():
        views = 0
        for j in i.articles.all():
            views += j.views
        rank[i.username] = views
    sorted_rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    result = []
    for i in sorted_rank:
        a = list(i)
        a.insert(0, index)
        user = User.objects.get(username=i[0])
        if user.photos.all():
            a.append(user.photos.all()[0].photo.url)
        else:
            a.append('https://alumni.tcnj.edu/wp-content/uploads/sites/16/2022/06/user-icon-placeholder.png')
        result.append(a)
        index = index + 1

    context = {
        'result': result[:100],
        'title': 'RANKING'
    }

    return render(request, 'ranking.html', context)


def save_like(request, article_slug):
    articles = []
    article = Article.objects.get(slug=article_slug)
    for i in Liked.objects.filter(user=request.user):
        articles.append(i.article)
    if article not in articles:
        article.like -= 1
        article.save()
        return redirect('article_detail', article.slug)
    else:
        article.like += 1
        article.save()
        return redirect('article_detail', article.slug)


def liked(request, slug):
    article = Article.objects.get(slug=slug)
    user = request.user
    like = Liked(article=article, user=user)
    try:
        a = Liked.objects.get(article=article, user=user)
        a.delete()
        return redirect('save_like', article.slug)
    except:
        like.save()
        return redirect('save_like', article.slug)


def photo_delete(request):
    try:
        user = request.user
        photo = AccountPhoto.objects.get(user=user)
        photo.delete()
        return redirect('profile')
    except:
        return redirect('profile')


def favourite(request):
    articles = []
    article = Liked.objects.filter(user=request.user)
    for i in article:
        articles.append(i.article)
    context = {
        'articles': articles,
        'title': 'LIKED'
    }

    return render(request, 'liked.html', context)


def saved_message(request):
    a = request.POST.get('message')
    photo = request.FILES.get('photo')
    if a and photo:
        a = Saved.objects.create(text=a, user=request.user, photo=photo)
        a.save()
        return redirect('saved_message')
    elif photo:
        a = Saved.objects.create(photo=photo, user=request.user)
        a.save()
        return redirect('saved_message')
    elif a:
        a = Saved.objects.create(text=a, user=request.user)
        a.save()
        return redirect('saved_message')
    messages = Saved.objects.filter(user=request.user)
    context = {
        'title': 'Saved Message',
        'messages': messages
    }

    return render(request, 'saved_message.html', context)


def share_post(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    if article.photo:
        image = article.photo.url
    else:
        image = 'https://avatars.mds.yandex.net/i?id=adc64fa49b3479a0bf526527b9f2ba882ba3c8e9-10928745-images-thumbs&n=13'
    a = request.GET.get('share')
    b = str(a).split()
    if b[0] == 'chat':
        c = Message.objects.create(is_share=True, message=f'{article.title}', user=request.user,
                                   chat=Chat.objects.get(slug=b[1]), image=image, url=f'{article.slug}')
        c.save()
        return redirect('message', b[1])
    if a == 'saved':
        if article.photo:
            b = Saved.objects.create(text=article.title, user=request.user, is_share=True, image=article.photo.url, url=f'{article.slug}')
        else:
            b = Saved.objects.create(text=article.title, user=request.user, is_share=True, image='https://avatars.mds.yandex.net/i?id=adc64fa49b3479a0bf526527b9f2ba882ba3c8e9-10928745-images-thumbs&n=13', url=f'{article.slug}')
        b.save()
        return redirect('saved_message')
    Chats = []

    chat1 = Chat.objects.filter(user1=request.user)
    chat2 = Chat.objects.filter(user2=request.user)
    chat3 = [chat1, chat2]
    for i in chat3:
        for j in i:
            Chats.append(j)

    context = {
        'chats': Chats,
        'title': 'Share'
    }

    return render(request, 'share.html', context)


def groups(request):
    len_member = {}
    groupss = []
    group = Group.objects.all()
    for i in group:
        len_member[i.group_name] = len(i.Members.all())
        for j in i.Members.all():
            if request.user == j.user:
                groupss.append(i)

    context = {
        'groups': groupss,
        'title': 'Group',
        'len_member': len_member
    }

    return render(request, 'groups.html', context)


def delete_invalid_group(request):
    for i in Group.objects.all():
        if len(i.Members.all()) == 0:
            i.delete()
    return redirect('groups')


def group_message(request, pk):
    group = Group.objects.get(pk=pk)
    if request.POST.get('message') and request.FILES.get('photo'):
        data = GroupMessage.objects.create(user=request.user, photo=request.FILES.get('photo'), group=group, message=request.POST.get('message'))
        data.save()
        return redirect('group_message', pk)
    elif request.method == 'POST' and request.FILES.get('photo'):
        data = GroupMessage.objects.create(user=request.user, photo=request.FILES.get('photo'), group=group)
        data.save()
        return redirect('group_message', pk)
    elif request.method == 'POST' and request.POST.get('message'):
        data = GroupMessage.objects.create(user=request.user, message=request.POST.get('message'), group=group)
        data.save()
        return redirect('group_message', pk)
    else:

        context = {
            'title': 'Group Message',
            'messages': GroupMessage.objects.filter(group=group),
            'group': group,
            'members': group.Members.all()
        }

        return render(request, 'group_message.html', context)


def add_member(request, pk):
    data = request.GET.get('search')
    if data:
        users = User.objects.filter(username__icontains=data)
    else:
        users = User.objects.all()
    group = Group.objects.get(pk=pk)
    user = request.GET.get('user')
    if user:
        try:
            GroupMember.objects.get(user=User.objects.get(username=user), group=group)
        except:
            new_user = User.objects.get(username=user)
            a = GroupMember.objects.create(user=new_user, group=group)
            a.save()
        return redirect('delete_invalid_group')
    context = {
        'users': users,
        'title': 'Add Member',
    }

    return render(request, 'add_member.html', context)


def exit_group(request, pk):
    group = Group.objects.get(pk=pk)
    a = GroupMember.objects.get(user=request.user, group=group)
    a.delete()
    return redirect('groups')


def create_group(request):
    photo = request.FILES.get('photo')
    group_name = request.POST.get('group_name')
    if group_name:
        if group_name and photo:
            data = Group.objects.create(group_name=group_name, photo=photo)
            data.save()
            member = GroupMember.objects.create(user=request.user, group=data)
            member.save()
            return redirect('group_message', data.id)
        else:
            data = Group.objects.create(group_name=group_name)
            data.save()
            member = GroupMember.objects.create(user=request.user, group=data)
            member.save()
            return redirect('group_message', data.id)
    else:
        return render(request, 'create_group.html', {'title': 'Create Group'})


def edit_group(request, pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=pk)
        group_name = request.POST.get('group_name')
        photo = request.FILES.get('photo')
        if group_name and photo:
            group.group_name = group_name
            group.photo = photo
            group.save()
            return redirect('groups')
        elif group_name:
            group.group_name = group_name
            group.save()
            return redirect('groups')
        elif photo:
            group.photo = photo
            group.save()
            return redirect('groups')
        else:
            return render(request, 'edit_group.html', {'title': 'Edit Group'})



    return render(request, 'edit_group.html', {'title': 'Change Photo'})


def channels(request):
    title = request.GET.get('channel')
    if title and title == 'other':
        channels = Channel.objects.all()
        data = 'Other Channels'
    elif title and title == 'my':
        data = 'My Channels'
        channels = Channel.objects.filter(admin=request.user)
    else:
        channels = Channel.objects.filter(Members__user=request.user)
        data = 'Subscriptions'

    context = {
        'channels': channels,
        'title': data
    }

    return render(request, 'channel.html', context)


def subscribe(request, pk):
    channel = Channel.objects.get(pk=pk)
    try:
        a = ChannelMember.objects.get(user=request.user, channel=channel)
        a.delete()
    except:
        a = ChannelMember.objects.create(user=request.user, channel=channel)
        a.save()
    return redirect('channels')


def create_channel(request):
    if request.method == 'POST':
        title = request.POST.get('group_name')
        photo = request.FILES.get('photo')
        data = Channel.objects.create(channel_name=title, photo=photo, admin=request.user)
        data.save()
        data1 = ChannelMember.objects.create(user=request.user, channel=data)
        data1.save()
        return redirect('channels')
    else:
        context = {
            'title': 'Create Channel',
        }
        return render(request, 'create_group.html', context)


def edit_channel(request, pk):
    if request.method == 'POST':
        title = request.POST.get('group_name')
        photo = request.FILES.get('photo')
        data = Channel.objects.get(pk=pk)
        if title and photo:
            data.channel_name = title
            data.photo = photo
            data.save()
            return redirect('channels')
        elif title:
            data.channel_name = title
            data.save()
            return redirect('channels')
        elif photo:
            data.photo = photo
            data.save()
            return redirect('channels')
        else:
            return redirect('channels')
    else:
        context = {
            'title': 'Edit Channel',
        }
        return render(request, 'create_group.html', context)


def channel_content(request, pk):
    channel = Channel.objects.get(pk=pk)
    content = ChannelContent.objects.filter(channel=channel)

    context = {
        'channel': channel,
        'contents': content,
        'title': channel.channel_name
    }

    return render(request, 'channel_content.html', context)


def channel_content_save(request, pk):
    channel = Channel.objects.get(pk=pk)
    if request.method == 'POST':
        data = ChannelContent.objects.create(content=request.POST.get('content'), channel=channel, image=request.FILES.get('photo'))
        data.save()
        return redirect('channel_content', pk)


def delete_channel(request, pk):
    data = request.GET.get('action')
    if data and data == 'yes':
        data1 = Channel.objects.get(pk=pk)
        data1.delete()
        return redirect('channels')
    if data and data == 'no':
        return redirect('channels')
    return render(request, 'yes_or_not.html', {'title': 'DELETE | CHANNEL'})
