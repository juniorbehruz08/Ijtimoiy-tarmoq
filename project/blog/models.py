from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Category')
    slug = models.SlugField(blank=True, verbose_name="Slug")
    image = models.ImageField(blank=True, null=True, verbose_name='Image')
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_photo(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def get_count(self):
        if self:
            return len(self.category.all())
        else:
            return '0'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    title = models.CharField(max_length=75, verbose_name="Article Title")
    content = models.TextField(verbose_name='About Article')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Picture')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Updated Date')
    views = models.IntegerField(default=0, verbose_name='Views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    slug = models.SlugField(blank=True, verbose_name='Slug', max_length=100)
    like = models.IntegerField(default=0, verbose_name='likes')

    objects = models.Manager()

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://avatars.mds.yandex.net/i?id=adc64fa49b3479a0bf526527b9f2ba882ba3c8e9-10928745-images-thumbs&n=13'

    def get_comment_count(self):
        if self.comments:
            return len(self.comments.all())
        else:
            return '0'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Article', related_name='comments')
    comment = models.TextField(verbose_name='Comment')
    date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'author = {self.author} | text = {self.comment} | article = {self.article.title}'


class AccountPhoto(models.Model):
    photo = models.ImageField(upload_to='AccountPhotos', verbose_name='photo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    objects = models.Manager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Account Photo'
        verbose_name_plural = 'Account Photos'


@receiver(pre_delete, sender=AccountPhoto)
def delete_image(sender, instance, **kwargs):
    instance.photo.delete()


@receiver(pre_delete, sender=Article)
def delete_image(sender, instance, **kwargs):
    instance.photo.delete()


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user1', related_name='user')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user2')
    slug = models.SlugField(blank=True, verbose_name='slug')
    objects = models.Manager()

    def __str__(self):
        return f'{self.user2}'

    class Meta:
        verbose_name = 'chat'
        verbose_name_plural = 'chats'


class Message(models.Model):
    message = models.CharField(max_length=1000, verbose_name='message')
    url = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, verbose_name='image', default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='time')
    is_share = models.BooleanField(default=False, verbose_name='Is share')
    objects = models.Manager()

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'


class Liked(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='liked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    objects = models.Manager()

    def __str__(self):
        return f'{self.user} liked {self.article}'


class Problem(models.Model):
    problem = models.CharField(max_length=1000, verbose_name='Problem')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.problem

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'


class Advertisement(models.Model):
    customer = models.CharField(max_length=200)
    video = models.FileField(upload_to='advertisement', verbose_name='Video', blank=True, null=True)
    image = models.ImageField(upload_to='advertisement', verbose_name='image')
    text = models.CharField(max_length=200, default='')
    url = models.CharField(max_length=500, default='')
    price = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return f'{self.customer}: {self.price}$'

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


class Saved(models.Model):
    text = models.CharField(max_length=1000, verbose_name='Saved Message')
    url = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, verbose_name='image', default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    is_share = models.BooleanField(default=False, verbose_name='Is share')
    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Group(models.Model):
    group_name = models.CharField(max_length=200, verbose_name='Group name')
    objects = models.Manager()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='time')
    photo = models.ImageField(upload_to='GroupPhoto', blank=True, null=True, verbose_name='photo')

    def get_len(self):
        a = Group.objects.get(group_name=self.group_name)
        b = a.Members.all()
        return len(b)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='Members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user}: {self.group}'

    class Meta:
        verbose_name = 'Group Member'
        verbose_name_plural = 'Group Members'


class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=1000, verbose_name='Message')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    is_share = models.BooleanField(default=False, verbose_name='Is share')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='time')
    objects = models.Manager()

    def __str__(self):
        return f'{self.user}: {self.message}'

    class Meta:
        verbose_name = 'Group Message'
        verbose_name_plural = 'Group Messages'


@receiver(pre_delete, sender=Group)
def delete_image(sender, instance, **kwargs):
    instance.photo.delete()


class Channel(models.Model):
    channel_name = models.CharField(max_length=200, verbose_name='Channel name')
    objects = models.Manager()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    photo = models.ImageField(upload_to='channelPhotos', verbose_name='Photo', blank=True, null=True)

    def total_follower(self):
        return len(self.Members.all()) - 1

    def __str__(self):
        return f'{self.channel_name} | Author:{self.admin}'

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'


@receiver(pre_delete, sender=Channel)
def delete_image(sender, instance, **kwargs):
    instance.photo.delete()


class ChannelMember(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='Members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ChannelMember')
    objects = models.Manager()

    def __str__(self):
        return f'{self.user}: {self.channel}'

    class Meta:
        verbose_name = 'Channel Member'
        verbose_name_plural = 'Channel Members'


class ChannelContent(models.Model):
    image = models.ImageField(upload_to='channelContentPhotos', verbose_name='Photo', blank=True, null=True)
    content = models.TextField(verbose_name='Content')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='ChannelContent')
    objects = models.Manager()

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Channel Content'
        verbose_name_plural = 'Channel Contents'


@receiver(pre_delete, sender=ChannelContent)
def delete_image(sender, instance, **kwargs):
    instance.photo.delete()


class ChannelContentComment(models.Model):
    comment = models.TextField(verbose_name='Comment')
    content = models.ForeignKey(ChannelContent, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Comments')
    objects = models.Manager()

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


@receiver(pre_delete, sender=ChannelContentComment)
def delete_image(sender, instance, **kwargs):
    instance.photo.delete()
