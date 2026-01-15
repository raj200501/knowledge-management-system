import os


def _get_int(value, default):
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


class Config:
    DB_URL = os.getenv("KMS_DB_URL", "sqlite:///knowledge.db")
    ENV = os.getenv("KMS_ENV", "development")
    LOG_LEVEL = os.getenv("KMS_LOG_LEVEL", "INFO")
    PAGE_SIZE = _get_int(os.getenv("KMS_PAGE_SIZE"), 20)
    PORT = _get_int(os.getenv("KMS_PORT"), 5000)


config = Config()
