from typing import NamedTuple

import pytest

from src.steampie import (
    get_account_id_from_trade_url,
    get_steam_id_from_trade_url,
    get_token_from_trade_url,
    has_token_in_trade_url,
)


class TradeUrlCase(NamedTuple):
    trade_url: str
    steam_id: str
    account_id: str
    token: str | None = None


CASES = [
    TradeUrlCase(
        trade_url="https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR",
        steam_id="76561198253325712",
        account_id="293059984",
        token="0-l_idZR",
    ),
    TradeUrlCase(
        trade_url="https://steamcommunity.com/tradeoffer/new/?partner=1429518176&token=VWHYmi0X",
        steam_id="76561199389783904",
        account_id="1429518176",
        token="VWHYmi0X",
    ),
    TradeUrlCase(
        trade_url="https://steamcommunity.com/tradeoffer/new/?partner=1029290644&token=6WTDPgzZ",
        steam_id="76561198989556372",
        account_id="1029290644",
        token="6WTDPgzZ",
    ),
    TradeUrlCase(
        trade_url="https://steamcommunity.com/tradeoffer/new/?partner=1217175197&token=ROes-A86",
        steam_id="76561199177440925",
        account_id="1217175197",
        token="ROes-A86",
    ),
    TradeUrlCase(
        trade_url="https://steamcommunity.com/tradeoffer/new/?partner=146309272",
        steam_id="76561198106575000",
        account_id="146309272",
    ),
]

parametrize_cases = pytest.mark.parametrize("case", CASES, ids=[c.account_id for c in CASES])


@parametrize_cases
def test_get_account_id_from_trade_url(case: TradeUrlCase) -> None:
    assert get_account_id_from_trade_url(case.trade_url) == case.account_id


@parametrize_cases
def test_get_steam_id_from_trade_url(case: TradeUrlCase) -> None:
    assert get_steam_id_from_trade_url(case.trade_url) == case.steam_id


@parametrize_cases
def test_has_token_in_trade_url(case: TradeUrlCase) -> None:
    assert has_token_in_trade_url(case.trade_url) is (case.token is not None)


@parametrize_cases
def test_get_token_from_trade_url(case: TradeUrlCase) -> None:
    assert get_token_from_trade_url(case.trade_url) == case.token
