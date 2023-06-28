__DEFAULT_DB_URL__ = "mysql+pymysql://root:password@localhost:3306/db"


class Settings:
    def __init__(self, db_url: bool):
        self.db_url = db_url


settings = Settings(__DEFAULT_DB_URL__)
