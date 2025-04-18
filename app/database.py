"""
Database configuration for Peewee ORM
"""
import os
from dotenv import load_dotenv
from peewee import PostgresqlDatabase, SqliteDatabase, Model
import datetime

# Load environment variables
load_dotenv()

# Get database configuration from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

# Configure database
if DATABASE_URL and DATABASE_URL.startswith('postgresql://'):
    # Parse PostgreSQL connection string
    # Format: postgresql://username:password@hostname:port/database
    parts = DATABASE_URL.replace('postgresql://', '').split('/')
    credentials_host = parts[0].split('@')
    
    if len(credentials_host) == 2:
        credentials = credentials_host[0].split(':')
        host_port = credentials_host[1].split(':')
        
        username = credentials[0]
        password = credentials[1] if len(credentials) > 1 else None
        hostname = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 5432
        database = parts[1]
        
        # Create PostgreSQL database instance
        db = PostgresqlDatabase(
            database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
    else:
        # Fallback to SQLite if connection string is malformed
        db = SqliteDatabase('instance/site.db')
else:
    # Default to SQLite
    db = SqliteDatabase('instance/site.db')

# Base model class that uses our database
class BaseModel(Model):
    class Meta:
        database = db
