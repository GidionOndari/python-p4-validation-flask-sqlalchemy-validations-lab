from models import db, Author, Post
from app import app

with app.app_context():
    # Clear existing data
    Post.query.delete()
    Author.query.delete()
    db.session.commit()

    # Create a valid author
    author = Author(name="Ben", phone_number="1234567890")
    db.session.add(author)
    db.session.commit()  # Commit so we get a valid author.id

    # Create posts linked to the author
    content_250 = "A" * 250
    summary_250 = "T" * 250

    post1 = Post(
        title="Secret Why I love programming.",
        content=content_250,
        summary=summary_250,
        category="Non-Fiction",
        author_id=author.id
    )

    post2 = Post(
        title="You Won't Believe Why coding is fun.",
        content=content_250,
        summary=None,
        category="Fiction",
        author_id=author.id
    )

    db.session.add_all([post1, post2])
    db.session.commit()

    print("Seeding complete! 1 author and 2 posts added.")
