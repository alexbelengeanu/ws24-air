import uvicorn
from .web.settings import app_settings

def main() -> None:
    """
    Entrypoint for the API.

    :return: None
    """

    # Run the API.
    uvicorn.run(
        app_settings.startup_path,
        workers=app_settings.workers,
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.reload,
        log_level=app_settings.log_level,
        factory=app_settings.factory,
    )


if __name__ == "__main__":
    main()