from abc import ABC, abstractmethod


class Provider(ABC):
    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key
        self.headers = {}

    @abstractmethod
    def get_url_and_params(self, steam_id: str | int, app_id: int | str, context_id: int | str) -> tuple[str, dict]:
        pass
