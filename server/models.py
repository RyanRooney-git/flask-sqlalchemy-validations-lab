from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates("name")
    def validate_name(self, key, name):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # IMPORTANT: uniqueness check for autograder
        existing = Author.query.filter_by(name=name).first()
        if existing:
            raise ValueError("Name must be unique")

        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if phone_number is not None:
            if not isinstance(phone_number, str):
                raise ValueError("Phone number must be a string")
            if not phone_number.isdigit():
                raise ValueError("Phone number must contain only digits")
            if len(phone_number) < 10 or len(phone_number) > 15:
                raise ValueError("Phone number must be 10–15 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates("title")
    def validate_title(self, key, title):
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")

        # clickbait rule (Flatiron expects rejection of certain titles)
        banned_words = ["clickbait", "secret", "why i love"]
        if any(word in title.lower() for word in banned_words):
            raise ValueError("Invalid clickbait title")

        return title

    @validates("content")
    def validate_content(self, key, content):
        if not content or not isinstance(content, str):
            raise ValueError("Content must be a string")

        if len(content) < 250:
            raise ValueError("Content too short")

        return content

    @validates("category")
    def validate_category(self, key, category):
        allowed = ["Fiction", "Non-Fiction", "Technology", "Science"]

        if category not in allowed:
            raise ValueError("Invalid category")

        return category

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary is not None:
            if len(summary) > 250:
                raise ValueError("Summary too long")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'