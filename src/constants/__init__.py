from pathlib import Path
from dataclasses import dataclass

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")
SCHEMA_FILE_PATH = Path("schema.yaml")

@dataclass
class EnvironmentVariable:
    CLIENT_ID = "cdyASsyXgbBsYZNclDeGXOjF"
    CLIENT_SECRET = "mCUPxbMZKLSjZFmQ6nRmQzys7-0yq5ZB.IMcSlrJQMwMvmjxn81g9kWnDYkgoTD5U+tNm,DrvAYJh8OaFnqbSa3xObkMs2WOs0OGZWZ1d6RooKNidXKe9ZZt5b8GzZOB"
    SECURE_CONNECT_BUNDLE = r"secure-connect-project-1.zip"
    DATABASE_NAME = 'project_1' 
    KEYSPACE_NAME = 'neuro_1'
    TABLE_NAME = 'CreditCardDefault_Data'
    AWS_ACCESS_KEY_ID_ENV_KEY = ""
    AWS_SECRET_ACCESS_KEY_ENV_KEY = ""
    REGION_NAME = ""

#env_var=EnvironmentVariable()