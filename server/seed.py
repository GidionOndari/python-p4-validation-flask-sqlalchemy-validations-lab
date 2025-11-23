#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Author, Post

fake = Faker()

with app.app_context():

    Post.query.delete()
    Author.query.delete()

    # Create Authors
    authors = []
    for _ in range(25):
        name = fake.unique.name()  # ensures unique names
        author = Author(name=name, phone_number='1324543333')
        authors.append(author)

    db.session.add_all(authors)
    db.session.commit()

    # Create Posts
    posts = []
    for _ in range(25):
        author = rc(authors)
        post = Post(
            title='Secret banana',
            content='This is the content Secret' * 50,
            category='Fiction',
            summary='Summary Secret',
            author=author
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()
