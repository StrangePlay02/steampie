from .provider import Provider


class ExpressLoad(Provider):
    def __init__(self, api_key: str = ""):
        super().__init__(api_key)
        self.headers = {"X-API-Key": self.api_key, "User-Agent": "tf2-express"}

    def get_url_and_params(self, steam_id: str | int, app_id: int | str, context_id: int | str) -> tuple[str, dict]:
        url = f"https://api.express-load.com/inventory/{steam_id}/{app_id}/{context_id}"
        params = {}

        return url, params
