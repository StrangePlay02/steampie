import pytest

from src.steampie import account_id_to_steam_id, steam_id_to_account_id

STEAM_TO_ACCOUNT = {
    "76561198253325712": "293059984",
    "76561198106575000": "146309272",
    "76561198106569347": "146303619",
    "76561198106499596": "146233868",
    "76561198071709562": "111443834",
    "76561198121083428": "160817700",
    "76561198121133015": "160867287",
    "76561198068416637": "108150909",
    "76561198121120257": "160854529",
    "76561198121058719": "160792991",
    "76561198134195928": "173930200",
    "76561198134196028": "173930300",
    "76561198134213928": "173948200",
    "76561198135383828": "175118100",
    "76561198135383928": "175118200",
    "76561198135384028": "175118300",
    "76561198248561278": "288295550",
    "76561198216321907": "256056179",
    "76561198216443897": "256178169",
    "76561198216449399": "256183671",
}


@pytest.mark.parametrize("steam_id, account_id", STEAM_TO_ACCOUNT.items(), ids=list(STEAM_TO_ACCOUNT))
def test_account_id_to_steam_id(steam_id: str, account_id: str) -> None:
    assert account_id_to_steam_id(account_id) == steam_id
    assert account_id_to_steam_id(int(account_id)) == steam_id


@pytest.mark.parametrize("steam_id, account_id", STEAM_TO_ACCOUNT.items(), ids=list(STEAM_TO_ACCOUNT))
def test_steam_id_to_account_id(steam_id: str, account_id: str) -> None:
    assert steam_id_to_account_id(steam_id) == account_id
    assert steam_id_to_account_id(int(steam_id)) == account_id
