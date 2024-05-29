from decouple import config
    #claves para acceder a las funcionalidades
    #user: Admin
    #password:password
class Config:
    SECRET_KEY=config('SECRET_KEY')
    UPLOAD_FOLDER=config('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS=config('ALLOWED_EXTENSIONS')
    #MAX_CONTENT_LENGTH=config('MAX_CONTENT_LENGTH')
    SESSION_TYPE=config('SESSION_TYPE')

class DevelopmentConfig(Config):
    DEBUG = True



config = {
    'development': DevelopmentConfig,

}