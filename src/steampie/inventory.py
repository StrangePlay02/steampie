import requests

from .providers import PROVIDERS, Custom, SteamCommunity


class Inventory:
    def __init__(self, provider_name: str = "steamcommunity", api_key: str | None = None) -> None:
        # default to steamcommunity
        self.provider = SteamCommunity()

        # default to steam if no api_key is given
        if not api_key:
            return

        provider_name = provider_name.lower()

        # if provider_name is a url, assign it as a custom provider address
        if provider_name.startswith("http"):
            self.provider = Custom(api_key, provider_name)
            return

        # loop through providers create object
        for i in PROVIDERS:
            if provider_name == i.__name__.lower():
                # set the first found provider and then stop
                self.provider = i(api_key)
                break

    def fetch(self, steam_id: int | str, app_id: int | str = 440, context_id: int | str = 2) -> dict:
        url, params = self.provider.get_url_and_params(steam_id, app_id, context_id)
        response = requests.get(url, params=params, headers=self.provider.headers)

        try:
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
