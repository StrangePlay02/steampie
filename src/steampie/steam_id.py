import struct


# implementation from bukson's steampy
def account_id_to_steam_id(account_id: str | int) -> str:
    first_bytes = int(account_id).to_bytes(4, byteorder="big")
    last_bytes = 0x1100001.to_bytes(4, byteorder="big")
    return str(struct.unpack(">Q", last_bytes + first_bytes)[0])


# implementation from bukson's steampy
def steam_id_to_account_id(steam_id: str | int) -> str:
    buffer = int(steam_id).to_bytes(8, byteorder="big")[4:]
    return str(struct.unpack(">L", buffer)[0])
