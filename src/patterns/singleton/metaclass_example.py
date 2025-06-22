import os
from random import randint


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        print(f"ConfigManager initializing with random number: {randint(1, 100)}")
        self._load_config()

    def _load_config(self):
        self._config = {
            "api_key": os.getenv("API_KEY"),
            "debug_mode": os.getenv("DEBUG", "False").lower() == "true",
            "max_connections": int(os.getenv("MAX_CONN", "10")),
        }

    def get(self, key, default=None):
        return self._config.get(key, default)


class DatabaseConfigManager(ConfigManager):
    def __init__(self):
        print(
            f"DatabaseConfigManager initializing with random number: {randint(1, 100)}"
        )
        super().__init__()
        self._load_db_config()

    def _load_db_config(self):
        # Add database-specific configuration
        self._config.update(
            {
                "db_host": os.getenv("DB_HOST", "localhost"),
                "db_port": int(os.getenv("DB_PORT", "5432")),
                "db_name": os.getenv("DB_NAME", "myapp"),
            }
        )

    def get_db_url(self):
        return f"postgresql://{self.get('db_host')}:{self.get('db_port')}/{self.get('db_name')}"


if __name__ == "__main__":
    # Usage: Configuration loaded once, shared everywhere
    c1 = ConfigManager()
    c2 = ConfigManager()
    print(c1 == c2)  # Should be True, both are the same instance
    print(c1 is c2)  # Should also be True, both variables point to the same instance

    # Test DatabaseConfigManager singleton
    db1 = DatabaseConfigManager()
    db2 = DatabaseConfigManager()
    print(db1 == db2)  # Should be True
    print(db1 is db2)  # Should be True
    print(db1.get_db_url())  # Test functionality
