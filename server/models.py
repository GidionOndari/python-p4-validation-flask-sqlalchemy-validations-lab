from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)

    posts = db.relationship('Post', backref='author', lazy=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Author must have a name")
        # Ensure uniqueness
        existing = Author.query.filter_by(name=value.strip()).first()
        if existing:
            raise ValueError("Author name must be unique")
        return value.strip()

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(250))
    category = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    CLICKBAIT_WORDS = ["Secret", "Top", "Guess", "Won't Believe", "Amazing", "Shocking"]

    @validates('title')
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Post must have a title")
        if not any(word in value for word in self.CLICKBAIT_WORDS):
            raise ValueError(f"Post title must be clickbait (include one of {self.CLICKBAIT_WORDS})")
        return value.strip()

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Content must be at least 250 characters")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value is not None and len(value) > 250:
            raise ValueError("Summary cannot exceed 250 characters")
        return value

    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = ["Fiction", "Non-Fiction"]
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of {allowed_categories}")
        return value

    @validates('author_id')
    def validate_author_id(self, key, value):
        author = Author.query.get(value)
        if not value or not author:
            raise ValueError("Post must have a valid author_id")
        return value
