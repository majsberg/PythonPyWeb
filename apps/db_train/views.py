from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count


class TrainView(View):
    def get(self, request):
        # TODO Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])

        # TODO Какой автор имеет наибольшее количество опубликованных статей?
        counter = Entry.objects.values('author_id').annotate(total=Count('text')).order_by('total').reverse().first()
        print(counter)
        self.answer2 = Author.objects.values('last_name', 'first_name', 'middle_name').get(id=counter['author_id'])

        # TODO Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer3 = Entry.objects.values('text').filter(tags__name__in=['Кино', 'Музыка']).distinct()

        # TODO Сколько авторов женского пола зарегистрировано в системе?
        self.answer4 = Author.objects.filter(gender='ж').count()

        # TODO Какой процент авторов согласился с правилами при регистрации?
        relative = Author.objects.filter(status_rule=True).count() / Author.objects.count()
        self.answer5 = relative * 100

        # TODO Какие авторы имеют стаж от 1 до 5 лет?
        self.answer6 = AuthorProfile.objects.filter(stage__range=(1, 5)).values('author__username')

        # TODO Какой автор имеет наибольший возраст?
        max_age = Author.objects.aggregate(max_age=Max('age'))
        self.answer7 = Author.objects.values('last_name', 'first_name', 'middle_name', 'age').get(age=max_age['max_age'])

        # TODO Сколько авторов указали свой номер телефона?
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()

        # TODO Какие авторы имеют возраст младше 25 лет?
        self.answer9 = Author.objects.values('username', 'last_name', 'first_name', 'middle_name').filter(age__lt=25)

        # TODO Сколько статей написано каждым автором?
        self.answer10 = Entry.objects.values('author__username').annotate(count=Count('text')).order_by('count')
        print(self.answer10)
        # for index in counter:
        #     print(f"idx = {index.get('author__username')}, value = {index.get('count')}")
        #self.answer10 = Author.objects.values('username').filter(id=index.get('author_id'))


        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}
        # Создайте здесь запросы к БД
        return render(request, 'train_db/training_db.html', context=context)

