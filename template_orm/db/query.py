from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    users_lst = [
        User(first_name='u1', last_name='u1'),
        User(first_name='u2', last_name='u2'),
        User(first_name='u3', last_name='u3'),
    ]
    User.objects.bulk_create(users_lst)

    blog_lst = [
        Blog(title='blog1', author=User.objects.get(first_name='u1')),
        Blog(title='blog2', author=User.objects.get(first_name='u1'))
    ]
    Blog.objects.bulk_create(blog_lst)

    topic_lst = [
        Topic(title='topic1', blog=Blog.objects.get(title='blog1'), author=User.objects.get(first_name='u1')),
        Topic(
            title='topic2_content', blog=Blog.objects.get(title='blog1'), author=User.objects.get(first_name='u3'),
            created='2017-01-01'
            )
    ]
    Topic.objects.bulk_create(topic_lst)

    blog1 = Blog.objects.get(title='blog1')
    blog1.subscribers.add(User.objects.get(first_name='u1'), User.objects.get(first_name='u2'))
    blog1.save()

    blog2 = Blog.objects.get(title='blog2')
    blog2.subscribers.add(User.objects.get(first_name='u2'))
    blog2.save()

    topic1 = Topic.objects.get(title='topic1')
    topic1.likes.add(
        User.objects.get(first_name='u1'),
        User.objects.get(first_name='u2'),
        User.objects.get(first_name='u3')
        )
    topic1.save()


'''
Поменять first_name на uu1 у всех пользователей (функция edit_all).
Поменять first_name на uu1 у пользователей, у которых first_name u1 или u2 (функция edit_u1_u2).
'''


def edit_all():
    users = User.objects.all()
    for user in users:
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    users = User.objects.filter(Q(first_name='u1') | Q(first_name='u2')).all()
    for user in users:
        user.first_name = 'uu1'
        user.save()


'''
удалить пользователя с first_name u1 (функция delete_u1).
отписать пользователя с first_name u2 от блогов (функция unsubscribe_u2_from_blogs).
'''


def delete_u1():
    user = User.objects.get(first_name='u1')
    user.delete()
    # user.save()


def unsubscribe_u2_from_blogs():
    user = User.objects.get(first_name='u2')
    subscribers = Blog.objects.filter(subscribers=user).all()

    for sub in subscribers:
        sub.subscribers.remove(user)


'''
Получить 2х первых пользователей (сортировка в обратном порядке по id) (функция get_user_with_limit).
Получить количество топиков в каждом блоге, назвать поле topic_count, отсортировать по topic_count по возрастанию (функция get_topic_count).
Получить среднее количество топиков в блоге (функция get_avg_topic_count).
Найти блоги, в которых топиков больше одного (функция get_blog_that_have_more_than_one_topic).
Получить все топики автора с first_name u1 (функция get_topic_by_u1).
Найти пользователей, у которых нет блогов, отсортировать по возрастанию id (функция get_user_that_dont_have_blog).
Найти топик, который лайкнули все пользователи (функция get_topic_that_like_all_users).
Найти топики, у которы нет лайков (функция get_topic_that_dont_have_like).'''


def get_topic_created_grated():
    result = Topic.objects.filter(created__gt='2018-01-01').all()

    return result


def get_topic_title_ended():
    result = Topic.objects.filter(title__endswith='content').all()

    return result


def get_user_with_limit():
    result = User.objects.order_by('id')

    return result.reverse()[:2]


def get_topic_count():
    top_count = Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')

    return top_count


def get_avg_topic_count():
    avg_count = Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))

    return avg_count


def get_blog_that_have_more_than_one_topic():
    result = Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)

    return result


def get_topic_by_u1():

    return Topic.objects.filter(author=User.objects.get(first_name='u1'))


def get_user_that_dont_have_blog():
    user = User.objects.annotate(blog_count=Count('blog')).filter(blog_count__exact=0)

    return user


def get_topic_that_like_all_users():
    topics = Topic.objects.all()

    return topics.filter(likes__in=User.objects.all()).distinct()


def get_topic_that_dont_have_like():
    topics = Topic.objects.all()

    return topics.exclude(likes__gt=0)

'''
solution
# query.py

from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    u1 = User.objects.create(first_name='u1', last_name='u1')
    u2 = User.objects.create(first_name='u2', last_name='u2')
    u3 = User.objects.create(first_name='u3', last_name='u3')

    b1 = Blog.objects.create(title='blog1', author=u1)
    b2 = Blog.objects.create(title='blog2', author=u1)

    b1.subscribers.add(u1, u2)
    b2.subscribers.add(u2)

    t1 = Topic.objects.create(title='topic1', blog=b1, author=u1)
    t2 = Topic.objects.create(
        title='topic2_content', blog=b1, author=u3,
        created=datetime(year=2017, month=1, day=1, tzinfo=UTC)
    )

    t1.likes.add(u1, u2, u3)


def edit_all():
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    User.objects.filter(
        Q(first_name='u1') | Q(first_name='u2')
    ).update(first_name='uu1')


def delete_u1():
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    Blog.subscribers.through.objects.filter(user__first_name='u2').delete()


def get_topic_created_grated():
    return Topic.objects.filter(created__gt=datetime(year=2018, month=1, day=1,
                                                     tzinfo=UTC))


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.all().order_by('-id')[:2]


def get_topic_count():
    return Blog.objects.annotate(
        topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(
        avg=Avg('topic_count')
    )


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.annotate(
        topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.filter(blog__isnull=True).order_by('pk')


def get_topic_that_like_all_users():
    count = User.objects.count()
    return Topic.objects.annotate(like=Count('likes')).filter(like=count)


def get_topic_that_dont_have_like():
    return Topic.objects.filter(likes__isnull=True)


'''