import tasks  # noqa

beat_schedule = {
    'fetch_prices': {
        "task": "tasks.fetch_prices",
        "schedule": 60,
    }
}
