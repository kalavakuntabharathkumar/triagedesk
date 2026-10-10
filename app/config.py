from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
 app_name:str="TriageDesk API"
 mongodb_url:str=""
 mongodb_database:str="triagedesk"
 llm_enabled:bool=False
 llm_api_key:str=""
 llm_api_url:str=""
 model_config=SettingsConfigDict(env_file=".env",extra="ignore",case_sensitive=False)
settings=Settings()
