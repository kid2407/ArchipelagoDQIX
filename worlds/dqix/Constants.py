from typing import NamedTuple


class AddressData(NamedTuple):
    address: int
    byte_size: int


class DQIXConstants:
    VISITED_LOCATIONS = AddressData(address=0x108910, byte_size=3)
    LEARNED_PARTY_TRICKS = AddressData(address=0x108A50, byte_size=4)
    UNLOCKABLE_VOCATIONS = AddressData(address=0x108AF8, byte_size=2)
    SPENT_MINIMEDALS = AddressData(address=0x0F5F7C, byte_size=4)
    GOLD_IN_BANK = AddressData(address=0x0F6D44, byte_size=4)
    GOLD_AT_HAND = AddressData(address=0x0F6D48, byte_size=4)

    # Common Items (Bag)
    COMMON_ITEMS_TYPE_START = AddressData(address=0x0F5DE8, byte_size=2)
    COMMON_ITEMS_TYPE_END = AddressData(address=0x0F5F16, byte_size=2)
    COMMON_ITEMS_COUNTS_START = AddressData(address=0x0F5F18, byte_size=1)
    COMMON_ITEMS_COUNTS_END = AddressData(address=0x0F5FAF, byte_size=1)

    # Weapons (Bag)
    WEAPONS_TYPE_START = AddressData(address=0x0F5FB0, byte_size=2)
    WEAPONS_TYPE_END = AddressData(address=0x0F61CE, byte_size=2)
    WEAPONS_COUNTS_START = AddressData(address=0x0F61D0, byte_size=1)
    WEAPONS_COUNTS_END = AddressData(address=0x0F61DF, byte_size=1)

    # Shields (Bag)
    SHIELDS_TYPE_START = AddressData(address=0x0F62E0, byte_size=2)
    SHIELDS_TYPE_END = AddressData(address=0x0F633E, byte_size=2)
    SHIELDS_COUNTS_START = AddressData(address=0x0F6340, byte_size=1)
    SHIELDS_COUNTS_END = AddressData(address=0x0F636F, byte_size=1)

    # Torso (Bag)
    TORSO_TYPE_START = AddressData(address=0x0F6370, byte_size=2)
    TORSO_TYPE_END = AddressData(address=0x0F64EE, byte_size=2)
    TORSO_COUNTS_START = AddressData(address=0x0F64F0, byte_size=1)
    TORSO_COUNTS_END = AddressData(address=0x0F65AF, byte_size=1)

    # Legs (Bag)
    LEGS_TYPE_START = AddressData(address=0x0F65B0, byte_size=2)
    LEGS_TYPE_END = AddressData(address=0x0F666E, byte_size=2)
    LEGS_COUNTS_START = AddressData(address=0x0F6670, byte_size=1)
    LEGS_COUNTS_END = AddressData(address=0x0F66CF, byte_size=1)

    # Headwear (Bag)
    HEADWEAR_TYPE_START = AddressData(address=0x0F66D0, byte_size=2)
    HEADWEAR_TYPE_END = AddressData(address=0x0F67EE, byte_size=2)
    HEADWEAR_COUNTS_START = AddressData(address=0x0F67F0, byte_size=1)
    HEADWEAR_COUNTS_END = AddressData(address=0x0F687F, byte_size=1)

    # Arms (Bag)
    ARMS_TYPE_START = AddressData(address=0x0F6880, byte_size=2)
    ARMS_TYPE_END = AddressData(address=0x0F691E, byte_size=2)
    ARMS_COUNTS_START = AddressData(address=0x0F6920, byte_size=1)
    ARMS_COUNTS_END = AddressData(address=0x0F696F, byte_size=1)

    # Footwear (Bag)
    FOOTWEAR_TYPE_START = AddressData(address=0x0F6970, byte_size=2)
    FOOTWEAR_TYPE_END = AddressData(address=0x0F6A4E, byte_size=2)
    FOOTWEAR_COUNTS_START = AddressData(address=0x0F6A50, byte_size=1)
    FOOTWEAR_COUNTS_END = AddressData(address=0x0F6A4E, byte_size=1)

    # Accessories (Bag)
    ACCESSORIES_TYPE_START = AddressData(address=0x0F6AC0, byte_size=2)
    ACCESSORIES_TYPE_END = AddressData(address=0x0F6B3E, byte_size=2)
    ACCESSORIES_COUNTS_START = AddressData(address=0x0F6B40, byte_size=1)
    ACCESSORIES_COUNTS_END = AddressData(address=0x0F6B7F, byte_size=1)

    # Important Items (Bag)
    IMPORTANT_ITEMS_TYPE_START = AddressData(address=0x0F6BEC, byte_size=2)
    IMPORTANT_ITEMS_TYPE_END = AddressData(address=0x0F6CA6, byte_size=2)
    IMPORTANT_ITEMS_COUNTS_START = AddressData(address=0x0F6CA8, byte_size=1)
    IMPORTANT_ITEMS_COUNTS_END = AddressData(address=0x0F6D05, byte_size=1)

    DQVC_MESSAGE = AddressData(address=0x0F9358, byte_size=510)
