from .custom import Custom
from .express_load import ExpressLoad
from .provider import Provider
from .steam_supply import SteamSupply
from .steamapis import SteamApis
from .steamcommunity import SteamCommunity

PROVIDERS: set[Provider] = {ExpressLoad, SteamSupply, SteamApis, SteamCommunity}

__all__ = [
    "PROVIDERS",
    "Custom",
    "ExpressLoad",
    "Provider",
    "SteamApis",
    "SteamCommunity",
    "SteamSupply",
]
