class Answer:
    def __init__(self, id, author, upvotes, text, is_correct, question_id):
        self._id = id
        self._author = author
        self._upvotes = upvotes
        self._text = text
        self._is_correct = is_correct
        self._question_id = question_id

    def __repr__(self):
        return f"Answer(id={self.id}, author={self._author}, upvotes={self._upvotes}, is_correct={self._is_correct}, question={self._question_id})"

    def id(self):
        return self._id

    def author(self):
        return self._author

    def upvotes(self):
        return self._upvotes

    def text(self):
        return self._text

    def is_correct(self):
        return self._is_correct

    def question_id(self):
        return self._question_id

def get_by_question_id(question_id):
    return list(filter(lambda a: a.question_id() == question_id, mock_answers))

mock_answers = [
    Answer(
        id=1,
        author='user123',
        upvotes=5,
        text='JSON (JavaScript Object Notation) — это формат обмена данными, широко используемый в веб-разработке.',
        is_correct=True,
        question_id=1
    ),
    Answer(
        id=2,
        author='dev_master',
        upvotes=8,
        text='JSON используется для передачи данных между клиентом и сервером в веб-приложениях.',
        is_correct=False,
        question_id=1
    ),
    Answer(
        id=3,
        author='data_guru',
        upvotes=2,
        text='JSON — это удобный для чтения людьми текстовый формат для представления структурированных данных.',
        is_correct=True,
        question_id=1
    ),
    Answer(
        id=4,
        author='api_expert',
        upvotes=10,
        text='REST API — это архитектурный стиль взаимодействия между клиентом и сервером с использованием стандартных HTTP-методов.',
        is_correct=True,
        question_id=2
    ),
    Answer(
        id=5,
        author='web_dev',
        upvotes=3,
        text='REST позволяет создать удобный и простой интерфейс для взаимодействия между сервисами.',
        is_correct=False,
        question_id=2
    ),
    Answer(
        id=6,
        author='coderlife',
        upvotes=7,
        text='Основные принципы REST — это клиент-серверная архитектура, отсутствие состояния и единообразие интерфейсов.',
        is_correct=True,
        question_id=2
    ),
    Answer(
        id=7,
        author='security_pro',
        upvotes=6,
        text='HTTPS обеспечивает шифрование данных при передаче, защищая от перехвата злоумышленниками.',
        is_correct=True,
        question_id=3
    ),
    Answer(
        id=8,
        author='network_guy',
        upvotes=4,
        text='HTTPS используется для безопасной передачи данных между клиентом и сервером.',
        is_correct=False,
        question_id=3
    ),
    Answer(
        id=9,
        author='techie',
        upvotes=12,
        text='Основное преимущество HTTPS в том, что он защищает данные и предотвращает их изменение.',
        is_correct=True,
        question_id=3
    ),
]

