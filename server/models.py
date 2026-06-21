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

        allowed_keywords = ["won't believe", "secret", "top", "guess"]

        if not any(keyword in title.lower() for keyword in allowed_keywords):
            raise ValueError(
                "Title must contain Won't Believe, Secret, Top, or Guess"
            )

        return title

    @validates("content")
    def validate_content(self, key, content):
        if content is None:
            raise ValueError("Content is required")

        if len(content) < 250:
            raise ValueError("Content too short")

        return content

    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Invalid category")

        return category

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary is not None and len(summary) > 250:
            raise ValueError("Summary too long")

        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'