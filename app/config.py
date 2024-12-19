class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Generate a random SECRET_KEY
    SECRET_KEY = "ASB"