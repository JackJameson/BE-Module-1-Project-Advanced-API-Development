class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/mechanic_shop_db'
    Debug = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass