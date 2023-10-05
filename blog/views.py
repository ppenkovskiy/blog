from datetime import date

from django.shortcuts import render

posts = [
    {
        'slug': 'hike-in-the-mountains',
        'image': 'mountains.jpg',
        'author': 'Me',
        'date': date(2023, 7, 21),
        'title': 'Mountain Hiking',
        'excerpt': "There's nothing like the views you get when hiking in the mountains!",
        'content': """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ad asperiores atque corporis culpa deleniti,
        deserunt distinctio, dolor dolore eius fugit harum labore maxime nisi perferendis quae quis ratione
        vel. Quam.
        """
    }
]


def starting_page(request):
    return render(request, "blog/index.html")


def posts(request):
    return render(request, "blog/all-posts.html")


def post_detail(request, slug):
    return render(request, 'blog/post-detail.html')
