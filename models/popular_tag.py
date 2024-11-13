class PopularTag:
    def __init__(self, id, title, size):
        self._id = id
        self._title = title
        self._size = size

    def __repr__(self):
        return f"PopularTag(id={self._id}, text={self._title}, size={self._size})"

    def id(self):
        return self._id

    def title(self):
        return self._title

    def size(self):
        return self._size

mock_popular_tags = [
    PopularTag(
        id = 1,
        title="Swift",
        size=12
    ),
    PopularTag(
        id = 2,
        title="Frontend",
        size = 10
    ),
    PopularTag(
        id = 3,
        title="JavaScript",
        size = 14
    ),
    PopularTag(
        id = 4,
        title="Python",
        size = 13
    ),
    PopularTag(
        id = 5,
        title="DevOps",
        size = 11
    ),
    PopularTag(
        id = 6,
        title="UI\\UX",
        size = 9
    ),
    PopularTag(
        id = 7,
        title="ML",
        size = 12
    ),
    PopularTag(
        id = 8,
        title="Backend",
        size = 10
    ),
    PopularTag(
        id = 9,
        title="SQL",
        size = 8
    ),
    PopularTag(
        id = 10,
        title="Data Science",
        size = 10
    )
]