from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  hard_limit: int = 1000

  model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

