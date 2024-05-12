import operator
import random

# from django.contrib.auth.models import User
from django.test import TestCase


# def ranking(request):
#     rank = {}
#     index = 1
#     for i in User.objects.all():
#         views = 0
#         for j in i.articles.all():
#             views += j.views
#         rank[i.username] = views
#     sorted_rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
#     result = []
#     for i in sorted_rank:
#         a = list(i)
#         a.insert(0, index)
#         user = User.objects.get(username=i[0])
#         if user.photos.all():
#             a.append(user.photos.all()[0].photo.url)
#         else:
#             a.append('https://alumni.tcnj.edu/wp-content/uploads/sites/16/2022/06/user-icon-placeholder.png')
#         result.append(a)
#         index = index + 1
#
#     context = {
#         'result': result
#     }
#
# ranking(10)
# a = ['6', '3', '5', '4']
# b = []
# while True:
#     c = ''
#     if len(b) == 24:
#         break
#     else:
#         while True:
#             if len(c) == 4:
#                 break
#             else:
#                 while True:
#                     if len(c) == 4:
#                         if c not in b:
#                             b.append(c)
#                         break
#                     d = random.randint(0, 3)
#                     data = a[d]
#                     print(data)
#                     print(c)
#                     if data not in c:
#                         c = c + data
#
#
# for i in b:
#     if int(i)%4 == 0:
#         print(i)