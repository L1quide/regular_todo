# mysite
**Установка Django**

`pip install Django==2.0.5`
_Проверяем версию Django в консоли_

`import django`
`django.get_version()`

**Создание первого проекта**
`django-admin startproject mysite`

**Создание миграций**

`cd mysite`
`python manage.py migrate`

**Запуск сервера для разработки**

`python manage.py runserver`

**Настройки проекта**

**Создание приложения**

`python manage.py startapp blog`

**Создание моделей**

_models.py_

**Активация приложения**
_Внастройку INSTALLED_APPS добавить_
`blog.apps.BlogConfig`

**Создание и применение миграций**
_Для начала необходимо создать инициализирующую миграцию для модели
Post._

`python manage.py makemigrations blog`

_Теперь синхронизируем базу данных._

`python manage.py migrate`

**С оздание сайта администрирования**

_Создание юзера_

`python manage.py createsuperuser`

_Запуск сервера_

`python manage.py runserver`

**Регистрация моделей в админке**

`from .models import Post`
`admin.site.register(Post)`

**Настройка отображения моделей**
`@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')`
_list_display - выводит список нужных нам полей.
@admin.register() регистрирует декорируемый класс – наследник ModelAdmin.
list_filter - отображает фильтр
search_fields - отображает строку поиска
date_hierarchy - отображает навигацию по датам
ordering - задает сортировку по умолчанию
prepopulated_fields - автоматическая генерация slug_

**Работа с Query Set и менеджерами**

_Создание объектов_

`user = User.objects.**get**(username='admin')
post = Post(title='Another post', slug='another-post',
body='Post body.', author=user)
post.**save()**`

_**get()** - возвращает единственный объект из базы данных._
_**DoesNotExist** - если get() не вернет объект из базы._
_**MultipleObjectsReturned** - если get() вернет несколько объектов из базы._
_**post.save()** - сохраняем статью в базу данных._
_**create()** - обьединяет создание и сохранение_

`Post.objects.create(title='One more post', slug='one-more-post',
body='Post body.', author=user)`

**Изменение объектов**

`post.title = 'New title'
post.save()`

**Получение объектов**

`all_posts = Post.objects.all()`

_**all()** - получает все объекты из базы_

_**Использование метода filter()**_

`Post.objects.filter(publish__year=2017)`

_**filter()** - фильтрация выборки._

**_Использование метода exclude()_**

`Post.objects.filter(publish__year=2017).exclude(title__startswith='Why')`

_**exclude()** - исключает данные из выборки._

**_Использование order_by()_**

_**order_by()** - сортировка запроса._

_Можно сортировать и в обратном порядке_

`Post.objects.order_by('-title')`

**Удаление объектов**

`post = Post.objects.get(id=1)
post.delete()`

_**delete()** - удаляет объекты._

**Создание менеджера модели**

**_1_**`Post.objects.my_manager()`
_**2**_`Post.my_manager.all()`

_models.py_

`class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')`
        
`class Post(models.Model):
    ...
    objects = models.Manager()
    published = PublishedManager() # Наш новый менеджер. ` 
    
**Обработчики списка статей и страницы подробностей**      
_Обработчики Django – это простая Python-функция, которая получает веб-запрос и возвращает веб-ответ._

`def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})`
    
_Процессоры контекста – это вызываемые функции, которые добавляют в контекст переменные._  

**Добавление шаблонов URL’ов для обработчиков**

_Шаблоны URL’ов позволяют сопоставить адреса с обработчиками. Шаблон пред-
ставляет собой комбинацию из строки, описывающей адрес, обработчика и не-
обязательного названия, которое даст возможность обращаться к этому шабло-
ну на всех уровнях проекта._

_mysite/blog/urls.py_

`from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.post_detail, name='post_detail'),
]`

_mysite/mysite/urls.py_

`from django.urls import path, **include**
from django.contrib import admin
urlpatterns = [
path('admin/', admin.site.urls),
**path('blog/', include('blog.urls', namespace='blog')),**
]`

**Канонические URL’ы для моделей**
    _**from django.urls import reverse**_
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month,
                                                 self.publish.day, self.slug])
                                                 
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month,
                                                 self.publish.day, self.slug])
_reverse() -  дает возможность получать URL, указав имяшаблона и параметры._   

**Создание HTML- шаблонов для обработчиков**

_В Django встроен мощный язык шаблонов, который позволяет задать отобра­
жение данных. Он основывается на таких понятиях, как шаблонные теги, пере-
менные и фильтры:
шаблонные теги управляют процессом генерации HTML и выглядят так:
**{% tag %};**
переменные шаблона заменяются переданными в контекст значениями
в процессе формирования HTML и выглядят так: **{{ variable }};**
шаблонные фильтры позволяют изменять переменные контекста и вы-
глядят так: **{{ variable|filter }}.**_        

_mysite/blog/templates/blog/base.html_  

_**{% load static %}**_
_<!DOCTYPE html>_
_<html>_
_<head>_
    _<title>**{% block title %}{% endblock %}**</title>_
    _<link href="**{% static "css/blog.css" %}**" rel="stylesheet">_
_</head>_
_<body>_
    _<div id="content">_
        _**{% block content %}**_
        _**{% endblock %}**_
    _</div>_
    _<div id="sidebar">_
        _<h2>My blog</h2>_
    _<p>This is my blog.</p>_
    _</div>_
_</body>_
_</html>_

_**{% loadstatic %}** - импортирует шаблоные тег static.  
После чего можно использовать запись **{%static %}**._   
_**{% block content %} {% endblock %}** - выводит блок содержимого._
        

_post/list.html_

_**{% extends "blog/base.html" %}**_
_**{% block title %}My Blog{% endblock %}**_
_**{% block content %}**_
_<h1>My Blog</h1>_
_**{% for post in posts %}**_
_<h2>_
_<a href="**{{ post.get_absolute_url }}**">**{{ post.title }}**</a>_
_</h2>_
_<p class="date">Published **{{ post.publish }}** by **{{ post.author }}**</p>_
_{{ post.body|truncatewords:30|linebreaks }}_
_**{% endfor %}**_
_**{% endblock %}**_    

_**{% extends %}** - указываем, что list.html унаследован от базо-
вого шаблона blog/base.html._   

_Фильтр **truncatewords**  - обрезает текст после указанного количества слов._     
_Фильтр **linebreaks** -  преобразует вывод в HTML с переносами строки._            

**Добавление постраничного отображения**

_views.py_

`from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
`
`def post_list(request):
object_list = Post.published.all()
paginator = Paginator(object_list, 3) # По 3 статьи на каждой странице.
page = request.GET.get('page')
try:
posts = paginator.page(page)
exceptPageNotAnInteger:
Если страница не является целым числом, возвращаем первую страницу.
posts = paginator.page(1)
except EmptyPage:
Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
posts = paginator.page(paginator.num_pages)
return render(request,'blog/post/list.html', {'page': page, 'posts': posts})`
_Постраничное отображение работает следующим образом:_
_1)	мы инициализируем объект класса Paginator, указав количество объектов
на одной странице;_
_2)	извлекаем из запроса GET-параметр page, который указывает текущую
страницу;_
_3)	получаем список объектов на нужной странице с помощью метода page()
класса Paginator;_
_4)	если указанный параметр page не является целым числом, обращаемся
к первой странице. Если page больше, чем общее количество страниц, то
возвращаем последнюю;_
_5) передаем номер страницы и полученные объекты в шаблон._   
            
_mysite/blog/templates/pagination.html_    
        
<div class="pagination">
<span class="step-links">
{% if page.has_previous %}
<a href="?page={{page.previous_page_number}}">Previous</a>
{% endif %}
<span class="current">
Page {{ page.number }} of {{ page.paginator.num_pages }}.
</span>
{% if page.has_next %}
<a href="?page={{ page.next_page_number }}">Next</a>
{% endif %}
</span>
</div>

_blog/post/list.html_
`{% block content %}
...
{% include "pagination.html" with page=posts %}
{% endblock %}`


**Использование обработчиков - классов**
_Обработчик – это вызываемая функция, которая принимает запрос
и возвращает ответ._

_Использование класса – это альтернативный способ реализации обработчи-
ков._

`from django.views.generic import ListView`

`class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'`
    
_Обработчик **PostListView** является аналогом функции post_list. В этом фраг-
менте кода мы настроили ListView на выполнение следующих шагов:
1 использовать переопределенный QuerySet модели вместо получения
всех объектов. Вместо задания атрибута QuerySet мы могли бы указать
модель model=Post, и тогда Django, используя стандартный менеджер мо-
дели, получал бы объекты как Post.objects.all();
2 использовать posts в качестве переменной контекста HTML-шаблона,
в которой будет храниться список объектов. Если не указать атрибут con-
text_object_name, по умолчанию используется переменная object_list;
3 использовать постраничное отображение по три объекта на странице;
4 использовать указанный шаблон для формирования страницы. Если бы
мы не указали template_name, то базовый класс ListView использовал бы
шаблон blog/post_list.html._

_mysite/blog/urls.py_
`urlpatterns = [
    Обработчики приложения блога.
    path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.post_detail,name='post_detail'),
]`

_post/list.html_

`{% include "pagination.html" with page=page_obj %}`


**Создание Django-форм**
_В Django встроены два базовых класса форм:
Form– позволяет создавать стандартные формы;
ModelForm– дает возможность создавать формы по объектам моделей._

_mysite/blog/templates/blog/forms.py_

`from django import forms
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)`
_**required=False** - необязательное поле._
_**CharField (<inputtype="text">)** - текстовое поле._
_Каждый тип по умолчанию имеет виджет для отображения. Виджет может быть изменен с помощью параметра **widget**._

**Обработка данных формы**
`from .forms import EmailPostForm
def post_share(request, post_id):
    Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id,status='published')
    if request.method == 'POST':
        Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
    if form.is_valid():
        Все поля формы прошли валидацию.
        cd = form.cleaned_data
        ... Отправка электронной почты.
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html',
            {'post': post, 'form': form})`
            
_В этом фрагменте мы выполняем следующие действия:
  определяем функцию post_share, которая принимает объект запроса re-
quest и параметр post_id;
  вызываем функцию get_object_or_404() для получения статьи с указан-
ным идентификатором и убеждаемся, что статья опубликована;
  используем один и тот же обработчик для отображения пустой формы
и обработки введенных данных. Для разделения логики отображения
формы или ее обработки используется запрос request. Заполненная фор-
ма отправляется методом POST. Если метод запроса – GET, необходимо ото-
бразить пустую форму; если приходит запрос POST, обрабатываем данные
формы и отправляем их на почту._

**Отправка электронной почты с Django**
`EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_account@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True`
_Настройка SMTP- сервера:
    EMAIL_HOST – хост SMTP-сервера; по умолчанию localhost;
    EMAIL_PORT – порт SMTP-сервера; по умолчанию 25;
    EMAIL_HOST_USER – логин пользователя для SMTP-сервера;
    EMAIL_HOST_PASSWORD – пароль пользователя для SMTP-сервера;
    EMAIL_USE_TLS – использовать ли защищенное TLS-подключение;
    EMAIL_USE_SSL – использовать ли скрытое TLS-подключение._
    
_Тестирование в Django-консоли:_
_python manage.py shell_
from django.core.mail import send_mail
`send_mail('Django mail', 'This e-mail was sent with Django.',
'your_account@gmail.com', ['your_account@gmail.com'], fail_silently=False)`
_Функция send_mail() принимает в качестве обязательных аргументов тему,
сообщение, отправителя и список получателей. Указав дополнительный пара-
метр fail_silently=False, мы говорим, чтобы при сбое в отправке сообщения
было сгенерировано исключение. Если в результате выполнения вы увидите 1,
ваше письмо успешно отправлено._


`from .forms import EmailPostForm
def post_share(request, post_id):
     Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id,status='published')
    sent = False
    if request.method == 'POST':
         Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
         Все поля формы прошли валидацию.
        cd = form.cleaned_data
         Отправка электронной почты.
        post_url = request.build_absolute_uri(post.get_absolute_url())
        subject = '{} ({}) recommends you reading "
        {}"'.format(cd['name'], cd['email'], post.title)
        message = 'Read "{}" at {}\n\n{}\'s comments:
        {}'.format(post.title, post_url, cd['name'], cd['comments'])
        send_mail(subject, message, 'admin@myblog.com', [cd['to']])
        sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
        {'post': post, 'form': form, 'sent': sent})`

_mysite/blog/urls.py_

`urlpatterns = [
...
path('<int:post_id>/share/', views.post_share, name='post_share'),
]`

**Отображение форм в HTML-шаблонах**

_blog/templates/blog/post/_

`{% extends "blog/base.html" %}`
`{% block title %}Share a post{% endblock %}`
`{% block content %}`
`{% if sent %}`
    `<h1>E-mail successfully sent</h1>`
    `<p>"{{ post.title }}" was successfully sent to {{ form.cleaned_data.to }}.</p>`
`{% else %}`
    `<h1>Share "{{ post.title }}" by e-mail</h1>`
    `<form action="." method="post">`
        `{{ form.as_p }}`
        `{% csrf_token %}`
        `<input type="submit" value="Send e-mail">`
    `</form>`
`{% endif %}`
`{% endblock %}`

_Если мы хотим
выводить каждое поле по отдельности, можно итерировать по ним таким об-
разом:_

`{% for field in form %}`
`<div>`
`{{ field.errors }}`
`{{ field.label_tag }} {{ field }}`
`</div>`
`{% endfor %}`

_Тег **{% csrf_token %}** - скрытое поле с автоматически сге-
нерированным токеном для защиты от подделки межсайтовых запросов (Сross
Site Request Forgery – CSRF-атак)._


**Добавление подсистемы комментариев**

__1) создать модель для сохранения комментариев;_
2) создать форму для отправки и валидации комментариев;_
_3)	добавить обработчик, который будет проверять форму и сохранять ком-
ментарий;_
_4) добавить на страницу статьи список комментариев._


`class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)`
        
        
_**ForeignKey** - отношение определено как «один ко многим»_ 
_Атрибут **related_name** позволяет получить доступ к комментариям конкретной статьи._
_**comment.post** - обращаться к статье из комментария._
_**post.comments.all()**- обращаться к комментариям статьи._
_**active** - дает возможность скрывать некоторые комментарии._

После создания новой модели как всегда выполняем миграции:

`python manage.py makemigrations blog`

`python manage.py migrate`

_Теперь мы можем добавить новую модель на сайт администрирования для
управления комментариями через интерфейс._

_mysite/blog/admin.py_

`from .models import Post, Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')`
    
    
**Создание модельных форм**

_mysite/blog/forms.py_

`from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')`
        
_Все, что нужно для создания формы из модели, – указать, какую модель ис-
пользовать в опциях класса Meta. Django найдет нужную модель и автомати-
чески построит форму._   
_Cписки **fields** или **exclude** позволяют явно указать, какие использовать, а какие – нет._
  
  
**Обработка модельных форм**

_mysite/blog/views.py_

`from .models import Post, Comment
from .forms import EmailPostForm, CommentForm`

`def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,
    publish__month=month,publish__day=day)
    Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            Привязываем комментарий к текущей статье.
            new_comment.post = post
            Сохраняем комментарий в базе данных.
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form})`
        
_Метод **save()** создает объект модели, с которой связана форма, и со-
храняет его в базу данных._

_Если в качестве аргумента метода передать
**commit=False**, то объект будет создан, но не будет сохранен в базу данных._


**Добавление комментариев в шаблон статьи**

_post/detail.html_

_Отобразит общее количество комментариев._

`{% with comments.count as total_comments %}
    <h2>{{ total_comments }} comment{{ total_comments|pluralize }}</h2>
{% endwith %}`


_Тег {% with %} полезен в случаях, когда в шаблоне нам нужно несколько раз обращаться
к функциям, выполняющим запросы в базу данных или сложные вычисления._

_**pluralize** - шаблонный фильтр для отображения слова comment
во множественном числе, если это будет необходимо._

_Список комментариев._

`{% for comment in comments %}`
`<div class="comment">`
    `<p class="info">`
    `   Comment {{ forloop.counter }} by {{ comment.name }}`
        `{{ comment.created }}`
    `</p>`
    `{{ comment.body|linebreaks }}`
`</div>`
`{% empty %}`
    `<p>There are no comments yet.</p>`
`{% endfor %}`

_Наконец, необходимо отобразить форму или сообщение об успешно создан-
ном комментарии._

`{% if new_comment %}`
`<h2>Your comment has been added.</h2>`
`{% else %}`
`<h2>Add a new comment</h2>`
`<form action="." method="post">`
`{{ comment_form.as_p }}`
`{% csrf_token %}`
`<p><input type="submit" value="Add comment"></p>`
`</form>`
`{% endif %}`

_Если new_comment не существует, мы показываем
поля формы создания комментария, в противном случае отображаем сообще-
ние о его успешном сохранении._


**Добавление подсистемы тегов**

`pip install django_taggit==0.22.2`

_settings.py_
`
INSTALLED_APPS = [
    ...
    'blog.apps.BlogConfig',
    'taggit',
]`

_mysite/blog/models.py_

`from taggit.managers import TaggableManager
    class Post(models.Model):
        ...
        tags = TaggableManager()`

`python manage.py makemigrations blog`

`python manage.py migrate`

_Отображение тегов на странице статей._

_blog/post/list.html_

`<p class="tags">Tags: {{ post.tags.all|join:", " }}</p>`

_Шаблонный фильтр join работает так же, как Python-функция join(): соеди-
няет элементы в строку, указывая в промежутках заданную строку._

_mysite/blog/views.py_

`from taggit.models import Tag
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    ...
    return render(request, 'blog/post/list.html',{'page': page,'posts': posts, 'tag': tag})`
    
_1.	Принимаем необязательный аргумент tag_slug, который по умолчанию
равен None. Этот параметр будет задаваться в URL’е._
_2.	Внутри обработчика формируем начальный QuerySet, находим все опуб­
ликованные статьи и, если указан слаг тега, получаем соответствующий
объект модели Tag с помощью метода get_object_or_404()._
_3.	Наконец, фильтруем изначальный список статей и оставляем только те,
которые связаны с полученным тегом. Так как это связь «многие ко мно-
гим», необходимо фильтровать статьи по вхождению тегов в список те-
гов, который в нашем случае состоит из единственного элемента._

_mysite/blog/urls.py_

`path('', views.post_list, name='post_list'),`
`/# path('', views.PostListView.as_view(), name='post_list').`
`path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag')`
_blog/post/list.html_

`{% include "pagination.html" with page=posts %}`
_Добавьте следующий фрагмент выше цикла {% for %}:_
`{% if tag %}
    <h2>Posts tagged with "{{ tag.name }}"</h2>
{% endif %}`


_Теперь добавим теги для каждой статьи:_
`<p class="tags">`
`Tags:`
    `{% for tag in post.tags.all %}`
    `<a href="{% url "blog:post_list_by_tag" tag.slug %}">`
    `{{ tag.name }}`
`</a>`
    `{% if not forloop.last %}, {% endif %}`
    `{% endfor %}`
`</p>`


**Формирование списка рекомендованных статей**

_Для того чтобы получить статьи, похожие на текущую, необходимо выпол-
нить следующие шаги:_
_1) получить все теги для текущей статьи;_
_2) получить все статьи, которые связаны хотя бы с одним тегом;_
_3) исключить текущую статью из списка похожих, чтобы не дублировать ее;_
_4) отсортировать результат по количеству совпадений тегов;_
_5)	в случае, если две и более статьи имеют одинаковый набор тегов, выби-
рать ту из них, которая является самой новой;_
_6)	ограничить выборку тем количеством статей, которое мы хотим отобра-
жать в списке рекомендуемых._


_mysite/blog/views.py_

`from django.db.models import Count`

_Count - функция агрегации из Django, входит в пакет django.db.models
Она позволяет выполнять агрегирующий запрос для подсчета количества тегов на уровне базы данных.
Пакет django.db.models содержит еще несколько агрегирующих функций:
Avg – среднее значение;
Max – максимальное значение;
Min – минимальное значение;
Count – количество объектов._

`.# Формирование списка похожих статей.
post_tags_ids = post.tags.values_list('id', flat=True)
similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]`

_Этот код работает следующим образом:_
_1)	получает все ID тегов текущей статьи. Метод QuerySet’а values_list() воз-
вращает кортежи со значениями заданного поля. Мы указали flat=True,
чтобы получить «плоский» список вида [1, 2, 3, ...];_
_2)	получает все статьи, содержащие хоть один тег из полученных ранее, ис-
ключая текущую статью;_
_3)	использует функцию агрегации Count для формирования вычисляемого
поля same_tags, которое содержит определенное количество совпадаю-
щих тегов;_
_4) сортирует список опубликованных статей в убывающем порядке по ко-
личеству совпадающих тегов для отображения первыми максимально похо-
жих статей и делает срез результата для отображения только четырех статей._

`return render(request,
'blog/post/detail.html',
{'post': post,
'comments': comments,
'new_comment': new_comment,
'comment_form': comment_form,
'similar_posts': similar_posts})`

**Создание собственных тегов**

_simple_tag – обрабатывает данные и возвращает строку;_
_inclusion_tag – обрабатывает данные и возвращает сформированный
фрагмент шаблона. Шаблонные теги должны быть реализованы в рамках Django-приложения._

**_md templatetags_**
**_cd templatetags_**
**_md __init__.py_**
**`md blog_tags.py`**

_mysite/blog/templatetags/blog_tags.py_

`from django import template`
`from ..models import Post`

`register = template.Library()
@register.simple_tag
def total_posts():
return Post.published.count()`

`@register.simple_tag(name='my_tag')` _- явно указать имя тега. По умолчанию 
Django будет использовать название функции_

**Использование собственных тегов в шаблоне.**
 
_blog/templates/base.html_
 
`{% loadblog_tags %}`
 
_Теперь можно использовать тег для показа количества опубликованных статей, добавив **{% total_posts %}** в HTML-
шаблон таким образом:_

{% load blog_tags %}
{% load static %}
...
<p>This is my blog. I've written {% total_posts %} posts so far.</p>
...

**Инклюзивный тег.**

`@register.inclusion_tag('blog/post/latest_posts.html')`

def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]`
    
    return {'latest_posts': latest_posts}

_Функция принимает один дополнительный аргумент – count,  по умолчанию равный 5.
Чтобы задать любое другое количество статей, используйте такую запись: **{% show_latest_posts 3 %}**._

_blog/post/latest_posts.html._

<ul>
    {% for post in latest_posts %}
    <li><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul

Отображаем ненумерованный список статей, используя переменную
контекста latest_posts, которую получаем из тега.

<h3>Latest posts</h3>
{% show_latest_posts 3 %}

Простой шаблонный тег.

blog/templatetags/blog_tags.py
from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=5):
return Post.published.annotate(total_comments=Count('comments'))
.order_by('-total_comments')[:count]

blog/base.html

<h3>Most commented posts</h3>
{% get_most_commented_posts as most_commented_posts %}
<ul>
{% for post in most_commented_posts %}
<li><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>

Записываем результат в переменную с помощью ключевого слова as
и указываем после него имя переменной. Для того чтобы наиболее коммен-
тируемые статьи были доступны в шаблоне через переменную most_comment-
ed_posts, используем запись вида {% get_most_commented_postsasmost_commented_
posts %}. Затем отображаем их в ненумерованном списке.


**Создание собственных фильтров.**

Фильтр – это Python-функция,
которая принимает один или два аргумента. В первый передается изменяемая
переменная контекста, во второй – любая дополнительная переменная. Вто-
рой аргумент не является обязательным. 
Фильтр выглядит так: {{ variable|my_filter:"foo" }}.

Markdown – это синтаксис форматирования, который легко использовать прямо в тексте, к тому же он
может быть конвертирован в HTML.

pip install Markdown==2.6.11

blog/templatetags/blog_tags.py

from django.utils.safestring import mark_safe
import markdown

@register.filter(name='markdown')
def markdown_format(text):
return mark_safe(markdown.markdown(text))

По умолчанию Django не доверяет любому HTML, получаемому из переменных
контекста или фильтров. Единственное исключение – фрагменты, помеченные
с помощью mark_safe.

blog/post/list.html и blog/post/detail

{% loadblog_tags %}

post/detail.html

{{ post.body|linebreaks }} <=> {{ post.body|markdown }}

post/list.html

{{ post.body|truncatewords:30|linebreaks }} <=> {{ post.body|markdown|truncatewords_html:30 }}

**Добавление полнотекстового поиска**

Установка PostgreSQL

sudo apt-get install libpq-dev python-dev

sudo apt-get install postgresql postgresql-contrib

pip install psycopg2==2.7.4

Простые поисковые запросы

settings.py

INSTALLED_APPS = [
# ...
'django.contrib.postgres',
]

from blog.models import Post
Post.objects.filter(body__search='django')

Этот запрос использует PostgreSQL для создания вектора по полю body и фра-
зы поиска django. В результат попадают записи, соответствующие поисковому
вектору.

Поиск по нескольким полям
В этом случае необходимо определить SearchVector.

from django.contrib.postgres.search import SearchVector
from blog.models import Post
Post.objects.annotate(search=SearchVector('title', 'body')).filter(search='django')

Используя аннотацию и определив SearchVector для обоих полей, мы добав-
ляем функциональность поиска совпадений по заголовку и телу статей.

Полнотекстовый поиск – это дорогая операция. Если вы применяете его для несколь-
ких сотен записей и более, в базе данных необходимо определить индекс, состоящий
из столбцов, участвующих в поиске. Django предоставляет класс SearchVectorField для
такого поля модели.

Обработчик поиска

mysite/blog/forms.py
class SearchForm(forms.Form):
    query = forms.CharField()
    
mysite/blog/views.py

from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.published.annotate(
        search=SearchVector('title', 'body'),
        ).filter(search=query)
        return render(request, 'blog/post/search.html', {'form': form,
        'query': query,
        'results': results})

Шаблон для отображения формы и результатов поиска.
mysite/blog/templates/blog/post/search.html

{% extends "blog/base.html" %}
{% block title %}Search{% endblock %}
{% block content %}
{% if query %}
<h1>Posts containing "{{ query }}"</h1>
<h3>
{% with results.count as total_results %}
Found {{ total_results }} result {{ total_results|pluralize }}
{% endwith %}
</h3>
{% for post in results %}
<h4><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h4>
{{ post.body|truncatewords:5 }}
{% empty %}
<p>There are no results for your query.</p>
{% endfor %}
<p><a href="{% url "blog:post_search" %}">Search again</a></p>
{% else %}
<h1>Search for posts</h1>
<form action="." method="get">
{{ form.as_p }}
<input type="submit" value="Search">
</form>
{% endif %}
{% endblock %}

Так же как и в обработчике поиска, мы проверяем, была ли форма отправ-
лена с параметром query. Перед отправкой формы отображаем ее и кнопку по-
иска. После того как пользователь ввел поисковую фразу и нажал на кнопку,
показываем результат – количество найденных статей и фразу, по которой осу-
ществлялся поиск.

mysite/blog/urls.py

path('search/', views.post_search, name='post_search'),


Взвешенные запросы

Мы можем повысить значимость некоторых векторов, чтобы совпадения по
ним считались более релевантными, чем по остальным. Например, можно на-
строить поиск так, чтобы статьи с совпадениями в заголовке были в большем
приоритете перед статьями с совпадениями в содержимом.

mysite/blog/views.py

search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
search_query = SearchQuery(query)results = Post.objects.annotate(
rank=SearchRank(search_vector, search_query)
).filter(rank__gte=0.3).order_by('-rank')

По умолчанию используются веса D, C, B и A, которые соответствуют числам
0.1, 0.2, 0.4 и 1. Мы применили вес 1.0 для вектора по полю title и 0.4 – для век-
тора по полю body. В конце отбрасываем статьи с низким рангом и показываем
только те, чей ранг выше 0.3.
