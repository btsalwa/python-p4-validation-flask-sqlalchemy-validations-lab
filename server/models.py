from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')

    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author cannot be empty.")

        existing_author = Author.query.filter(Author.name == name).first()
        
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author with this name already exists.")
        return name 
        

    def validate_phone_number(self, key, value):
        if len(value) != 10:
            raise ValueError(f'{key} must be exactly 10 digits')
        return value

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

    # Add validators 
    @validates('titles', 'content', 'category', 'summary')
    
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title must contain one of the following: 'Won't Believe', 'Secret', 'Top [number]', 'Guess'")
        return title

    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError(f'{key} must be at least 250 characters')
        return content
    
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary cannot be more than 250 characters.")
        return summary
    
    def validate_category(self, key, category):
        if not category:
            raise ValueError("Post must have a category.")
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
