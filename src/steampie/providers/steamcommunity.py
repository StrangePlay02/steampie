from .provider import Provider


class SteamCommunity(Provider):
    def get_url_and_params(self, steam_id: str | int, app_id: int | str, context_id: int | str) -> tuple[str, dict]:
        url = f"https://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}"
        params = {"l": "english", "count": 2500}

        return url, params
