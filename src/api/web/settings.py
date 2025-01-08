from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    startup_path: str = "src.api.web.application:get_app"
    workers: int = 1
    host: str = "0.0.0.0"
    port: int = 5000
    reload: bool = True
    log_level: str = "debug"
    factory: bool = True

    # Database settings
    db_name: str = 'local.db'
    remove_if_exists: bool = False # Set to True to remove the database if it exists
    embedding_dim: int = 512
    similarity_metric: str = "COSINE"
    celeb_img_folder_path: str = "./data/img_align_celeba"
    celeb_identity_map_path: str = "./data/identity_CelebA.txt"
    max_results: int = 1

# Create an instance of the settings to be used throughout your FastAPI app
app_settings = Settings()