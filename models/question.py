class Question:
    def __init__(self, title, text, tags, id, author_id, upvotes, replies):
        self._id = id
        self._title = title
        self._author_id = author_id
        self._text = text
        self._tags = tags
        self._upvotes = upvotes
        self._replies = replies

    def __repr__(self):
        return f"Question(id={self._id}, title={self._title}, author={self._author_id}, upvotes={self._upvotes})"

    def id(self):
        return self._id

    def title(self):
        return self._title

    def author(self):
        return self._author_id

    def text(self):
        return self._text

    def tags(self):
        return self._tags

    def upvotes(self):
        return self._upvotes

    def replies(self):
        return self._replies


def get_by_id(question_id):
    for question in mock_questions:
        if question.id() == question_id:
            return question

def get_by_tag(question_tag):
    result = []
    for question in mock_questions:
        for tag in question.tags():
            print(tag)
            if tag == question_tag:
                result.append(question)
                break
    return result


mock_questions = [
    Question(
        id=1,
        author_id='tech_master',
        title='Что такое REST API?',
        text='Как работает REST и какие у него основные принципы?',
        tags=['rest', 'api', 'веб'],
        upvotes=10,
        replies=3
    ),
    Question(
        id=2,
        author_id='coder123',
        title='Какой смысл в использовании Docker?',
        text='Зачем нужен Docker и какие у него основные преимущества?',
        tags=['docker', 'контейнеризация', 'разработка'],
        upvotes=7,
        replies=5
    ),
    Question(
        id=3,
        author_id='dev_sasha',
        title='Что такое кэширование?',
        text='Как работает кэширование и где его лучше всего применять?',
        tags=['кэширование', 'оптимизация', 'веб'],
        upvotes=12,
        replies=1
    ),
    Question(
        id=4,
        author_id='programmer_olga',
        title='Как работают потоки в Python?',
        text='Объясните основы потоков и их реализацию в Python.',
        tags=['python', 'потоки', 'многозадачность'],
        upvotes=4,
        replies=7
    ),
    Question(
        id=5,
        author_id='data_analyst_99',
        title='Что такое JSON?',
        text='Как его парсить?',
        tags=['json', 'форматы данных', 'веб'],
        upvotes=3,
        replies=2
    ),
    Question(
        id=6,
        author_id='alex_dev',
        title='Зачем использовать тестирование?',
        text='Какие основные подходы к тестированию существуют?',
        tags=['тестирование', 'разработка', 'автоматизация'],
        upvotes=15,
        replies=6
    ),
    Question(
        id=7,
        author_id='backend_guru',
        title='Что такое микросервисы?',
        text='Объясните концепцию микросервисной архитектуры.',
        tags=['микросервисы', 'архитектура', 'веб'],
        upvotes=6,
        replies=3
    ),
    Question(
        id=8,
        author_id='qa_specialist',
        title='Как работают регулярные выражения?',
        text='Объясните, что такое регулярные выражения и как их применять.',
        tags=['регулярные выражения', 'текст', 'поиск'],
        upvotes=9,
        replies=4
    ),
    Question(
        id=9,
        author_id='ml_student',
        title='Что такое нейронная сеть?',
        text='Объясните принцип работы нейронных сетей.',
        tags=['машинное обучение', 'нейронные сети'],
        upvotes=13,
        replies=4
    ),
    Question(
        id=10,
        author_id='front_end_jane',
        title='Как работает Flexbox в CSS?',
        text='Объясните основные свойства Flexbox и их использование.',
        tags=['css', 'flexbox', 'веб-разработка'],
        upvotes=5,
        replies=5
    ),
    Question(
        id=11,
        author_id='system_admin',
        title='Что такое виртуализация?',
        text='Опишите, как работает виртуализация и её преимущества.',
        tags=['виртуализация', 'инфраструктура'],
        upvotes=8,
        replies=1
    ),
    Question(
        id=12,
        author_id='swift_lover',
        title='Как работает ARC в Swift?',
        text='Объясните Automatic Reference Counting и его принцип.',
        tags=['swift', 'память', 'разработка'],
        upvotes=6,
        replies=7
    ),
    Question(
        id=13,
        author_id='java_geek',
        title='Что такое JVM?',
        text='Объясните, как работает Java Virtual Machine и её функции.',
        tags=['java', 'jvm', 'виртуальная машина'],
        upvotes=7,
        replies=2
    ),
    Question(
        id=14,
        author_id='cyber_student',
        title='Что такое HTTPS?',
        text='Опишите, как работает HTTPS и зачем он нужен.',
        tags=['https', 'безопасность', 'веб'],
        upvotes=9,
        replies=7
    ),
    Question(
        id=15,
        author_id='network_ninja',
        title='Что такое VLAN?',
        text='Как работает VLAN и где его используют?',
        tags=['vlan', 'сеть', 'инфраструктура'],
        upvotes=11,
        replies=0
    ),
    Question(
        id=16,
        author_id='ios_developer',
        title='Что такое SwiftUI?',
        text='Объясните, как работает SwiftUI и его основные принципы.',
        tags=['swiftui', 'ios', 'ui-разработка'],
        upvotes=4,
        replies=1
    ),
    Question(
        id=17,
        author_id='dev_tim',
        title='Что такое веб-сокеты?',
        text='Как работают веб-сокеты и в чём их преимущество?',
        tags=['веб-сокеты', 'веб', 'реальное время'],
        upvotes=10,
        replies=12
    ),
    Question(
        id=18,
        author_id='tech_writer',
        title='Как работает OAuth?',
        text='Объясните принцип авторизации через OAuth и его использование.',
        tags=['oauth', 'безопасность', 'веб'],
        upvotes=5,
        replies=5
    ),
    Question(
        id=19,
        author_id='data_scientist_anna',
        title='Что такое DataFrame в Pandas?',
        text='Опишите структуру DataFrame и основные методы работы с ним.',
        tags=['pandas', 'dataframe', 'данные'],
        upvotes=6,
        replies=3
    ),
    Question(
        id=20,
        author_id='js_dev',
        title='Как работает замыкание в JavaScript?',
        text='Поясните, что такое замыкание и как оно используется в JS.',
        tags=['javascript', 'замыкания', 'функции'],
        upvotes=8,
        replies=1
    ),
    Question(
        id=21,
        author_id='linux_fan',
        title='Что такое sudo?',
        text='Зачем нужна команда sudo и как она работает?',
        tags=['linux', 'sudo', 'администрирование'],
        upvotes=4,
        replies=3
    ),
    Question(
        id=22,
        author_id='ml_researcher',
        title='Что такое кластеризация?',
        text='Опишите принципы кластеризации в машинном обучении.',
        tags=['машинное обучение', 'кластеризация', 'алгоритмы'],
        upvotes=12,
        replies=5
    ),
    Question(
        id=23,
        author_id='cloud_guru',
        title='Как работает Kubernetes?',
        text='Объясните, что такое Kubernetes и его основную архитектуру.',
        tags=['kubernetes', 'контейнеризация', 'облако'],
        upvotes=14,
        replies=2
    ),
    Question(
        id=24,
        author_id='ios_senior',
        title='Как использовать Combine в Swift?',
        text='Опишите, как работает фреймворк Combine и его применение.',
        tags=['swift', 'combine', 'асинхронность'],
        upvotes=7,
        replies=3
    ),
    Question(
        id=25,
        author_id='frontend_expert',
        title='Как работает DOM в браузере?',
        text='Объясните, что такое DOM и как он взаимодействует с JavaScript.',
        tags=['javascript', 'dom', 'веб-разработка'],
        upvotes=9,
        replies=7
    ),
    Question(
        id=26,
        author_id='blockchain_fan',
        title='Что такое блокчейн?',
        text='Объясните, как работает блокчейн и где он используется.',
        tags=['блокчейн', 'технологии', 'безопасность'],
        upvotes=13,
        replies=3
    ),
    Question(
        id=27,
        author_id='android_fan',
        title='Как работает Jetpack Compose?',
        text='Объясните основные принципы работы Jetpack Compose.',
        tags=['android', 'jetpack compose', 'ui-разработка'],
        upvotes=10,
        replies=3
    ),
    Question(
        id=28,
        author_id='dev_oleg',
        title='Что такое MVC?',
        text='Опишите модель MVC и где её применяют.',
        tags=['mvc', 'архитектура', 'разработка'],
        upvotes=5,
        replies=0
    ),
    Question(
        id=29,
        author_id='game_dev_nikita',
        title='Как работает физика в Unity?',
        text='Опишите, как работает физический движок в Unity.',
        tags=['unity', 'геймдев', 'физика'],
        upvotes=8,
        replies=6
    ),
    Question(
        id=30,
        author_id='cyber_security',
        title='Что такое DDoS-атака?',
        text='Объясните, как работает DDoS-атака и как от неё защититься.',
        tags=['безопасность', 'атаки', 'ddos'],
        upvotes=15,
        replies=9
    ),
]