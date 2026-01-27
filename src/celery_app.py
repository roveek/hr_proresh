import celery
import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):

    broker: str = pydantic.Field(
        'redis://localhost:6379/0', alias='CELERY_BROKER_URL')
    backend: str = pydantic.Field(
       'redis://localhost:6379/0', alias='CELERY_RESULT_BACKEND')


celery_app = celery.Celery(__name__, **Config().model_dump())
# celery_app = celery.Celery(__name__, **Config().model_dump())
celery_app.config_from_object('celeryconfig')
