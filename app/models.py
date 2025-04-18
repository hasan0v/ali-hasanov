"""
Peewee ORM models replacing SQLAlchemy models
"""
from peewee import (
    CharField, TextField, DateTimeField, BooleanField, 
    ForeignKeyField, IntegerField, FloatField, DateField, ManyToManyField
)
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .database import BaseModel, db
from slugify import slugify

# Create tables list to store all models
models = []

class User(BaseModel):
    username = CharField(max_length=64, unique=True, index=True)
    email = CharField(max_length=120, unique=True, index=True)
    password_hash = CharField(max_length=128)
    name = CharField(max_length=64, null=True)
    bio = TextField(null=True)
    profile_pic = CharField(max_length=120, null=True)
    role = CharField(max_length=20, default='user')  # 'admin', 'editor', 'user'
    created_at = DateTimeField(default=datetime.datetime.now)
    
    def get_id(self):
        """Flask-Login interface method"""
        return str(self.id)
    
    def is_authenticated(self):
        """Flask-Login interface method"""
        return True
    
    def is_active(self):
        """Flask-Login interface method"""
        return True
        
    def is_anonymous(self):
        """Flask-Login interface method"""
        return False
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

models.append(User)

class Category(BaseModel):
    name = CharField(max_length=64, unique=True)
    slug = CharField(max_length=64, unique=True, index=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

models.append(Category)

class Tag(BaseModel):
    name = CharField(max_length=64, unique=True)
    slug = CharField(max_length=64, unique=True, index=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

models.append(Tag)

class Post(BaseModel):
    title = CharField(max_length=255)
    slug = CharField(max_length=255, unique=True, index=True)
    content = TextField()
    summary = TextField()
    featured_image = CharField(max_length=255, null=True)
    published = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='posts')
    category = ForeignKeyField(Category, backref='posts', null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)

models.append(Post)

# Many-to-many relationship between Post and Tag
class PostTag(BaseModel):
    post = ForeignKeyField(Post, backref='post_tags')
    tag = ForeignKeyField(Tag, backref='tag_posts')
    
    class Meta:
        indexes = (
            (('post', 'tag'), True),  # Unique together
        )

models.append(PostTag)

class Service(BaseModel):
    title = CharField(max_length=100)
    slug = CharField(max_length=100, unique=True, index=True)
    description = TextField()
    short_description = TextField()
    image = CharField(max_length=255, null=True)
    featured = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.datetime.now()
        return super(Service, self).save(*args, **kwargs)

models.append(Service)

class ServicePlan(BaseModel):
    name = CharField(max_length=100)
    description = TextField()
    price = FloatField()
    currency = CharField(max_length=3, default='AZN')
    is_featured = BooleanField(default=False)
    service = ForeignKeyField(Service, backref='service_plans')

models.append(ServicePlan)

class Project(BaseModel):
    title = CharField(max_length=255)
    slug = CharField(max_length=255, unique=True, index=True)
    description = TextField()
    short_description = TextField()
    thumbnail = CharField(max_length=255, null=True)
    featured = BooleanField(default=False)
    client = CharField(max_length=100, null=True)
    completion_date = DateField(null=True)
    technologies_used = TextField(null=True)
    project_url = CharField(max_length=255, null=True)
    category = ForeignKeyField(Category, backref='projects', null=True) # Added category relationship
    created_at = DateTimeField(default=datetime.datetime.now)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Project, self).save(*args, **kwargs)

models.append(Project)

class ProjectImage(BaseModel):
    project = ForeignKeyField(Project, backref='images')
    image_url = CharField(max_length=255)
    caption = CharField(max_length=255, null=True)

models.append(ProjectImage)

class AITool(BaseModel):
    name = CharField(max_length=100)
    slug = CharField(max_length=100, unique=True, index=True)
    description = TextField()
    image = CharField(max_length=255, null=True)
    url = CharField(max_length=255, null=True)
    category = CharField(max_length=50, null=True)
    featured = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(AITool, self).save(*args, **kwargs)

models.append(AITool)

class Contact(BaseModel):
    name = CharField(max_length=100)
    email = CharField(max_length=120)
    subject = CharField(max_length=255)
    message = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    read = BooleanField(default=False)

models.append(Contact)

def create_tables():
    """Create database tables for all models"""
    with db:
        db.create_tables(models)
        
        # Check if the category_id column exists in the Project table
        # If not, add it. This is a basic migration approach.
        try:
            # Attempt to select the column to see if it exists.
            # Use the actual column name Peewee creates.
            db.execute_sql("SELECT category_id FROM project LIMIT 1;")
        except Exception as e: # Catch specific DB error if possible, e.g., peewee.ProgrammingError
            # Assuming the error means the column doesn't exist
            print(f"Attempting to add category_id column to Project table (error checking: {e})")
            try:
                # Use the correct column name 'category_id'
                db.execute_sql("ALTER TABLE project ADD COLUMN category_id INTEGER REFERENCES category(id);")
                print("category_id column added successfully.")
            except Exception as alter_e:
                print(f"Failed to add category_id column: {alter_e}")
                # Consider raising the error or logging it more formally

def init_db():
    """Initialize the database"""
    create_tables()
