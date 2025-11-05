from typing import NamedTuple


class AddressData(NamedTuple):
    address: str | int
    segment_size: int


class DQIXConstants:
    VISITED_LOCATIONS = AddressData(address=0x108910, segment_size=3)
    LEARNED_PARTY_TRICKS = AddressData(address=0x108A50, segment_size=4)
    UNLOCKABLE_VOCATIONS = AddressData(address=0x108AF8, segment_size=2)
    SPENT_MINIMEDALS = AddressData(address=0x0F5F7C, segment_size=4)
    GOLD_IN_BANK = AddressData(address=0x0F6D44, segment_size=4)
    GOLD_AT_HAND = AddressData(address=0x0F6D48, segment_size=4)

    # Common Items (Bag)
    COMMON_ITEMS_TYPE_START = AddressData(address=0x0F5DE8, segment_size=2)
    COMMON_ITEMS_TYPE_END = AddressData(address=0x0F5F16, segment_size=2)
    COMMON_ITEMS_COUNTS_START = AddressData(address=0x0F5F18, segment_size=1)
    COMMON_ITEMS_COUNTS_END = AddressData(address=0x0F5FAF, segment_size=1)
    COMMON_ITEMS_SEGMENTS = 152

    # Weapons (Bag)
    WEAPONS_TYPE_START = AddressData(address=0x0F5FB0, segment_size=2)
    WEAPONS_TYPE_END = AddressData(address=0x0F61CE, segment_size=2)
    WEAPONS_COUNTS_START = AddressData(address=0x0F61D0, segment_size=1)
    WEAPONS_COUNTS_END = AddressData(address=0x0F61DF, segment_size=1)
    WEAPONS_SEGMENTS = 272

    # Shields (Bag)
    SHIELDS_TYPE_START = AddressData(address=0x0F62E0, segment_size=2)
    SHIELDS_TYPE_END = AddressData(address=0x0F633E, segment_size=2)
    SHIELDS_COUNTS_START = AddressData(address=0x0F6340, segment_size=1)
    SHIELDS_COUNTS_END = AddressData(address=0x0F636F, segment_size=1)
    SHIELDS_SEGMENTS = 48

    # Torso (Bag)
    TORSO_TYPE_START = AddressData(address=0x0F6370, segment_size=2)
    TORSO_TYPE_END = AddressData(address=0x0F64EE, segment_size=2)
    TORSO_COUNTS_START = AddressData(address=0x0F64F0, segment_size=1)
    TORSO_COUNTS_END = AddressData(address=0x0F65AF, segment_size=1)
    TORSO_SEGMENTS = 192

    # Legs (Bag)
    LEGS_TYPE_START = AddressData(address=0x0F65B0, segment_size=2)
    LEGS_TYPE_END = AddressData(address=0x0F666E, segment_size=2)
    LEGS_COUNTS_START = AddressData(address=0x0F6670, segment_size=1)
    LEGS_COUNTS_END = AddressData(address=0x0F66CF, segment_size=1)
    LEGS_SEGMENTS = 96

    # Headwear (Bag)
    HEADWEAR_TYPE_START = AddressData(address=0x0F66D0, segment_size=2)
    HEADWEAR_TYPE_END = AddressData(address=0x0F67EE, segment_size=2)
    HEADWEAR_COUNTS_START = AddressData(address=0x0F67F0, segment_size=1)
    HEADWEAR_COUNTS_END = AddressData(address=0x0F687F, segment_size=1)
    HEADWEAR_SEGMENTS = 144

    # Arms (Bag)
    ARMS_TYPE_START = AddressData(address=0x0F6880, segment_size=2)
    ARMS_TYPE_END = AddressData(address=0x0F691E, segment_size=2)
    ARMS_COUNTS_START = AddressData(address=0x0F6920, segment_size=1)
    ARMS_COUNTS_END = AddressData(address=0x0F696F, segment_size=1)
    ARMS_SEGMENTS = 80

    # Footwear (Bag)
    FOOTWEAR_TYPE_START = AddressData(address=0x0F6970, segment_size=2)
    FOOTWEAR_TYPE_END = AddressData(address=0x0F6A4E, segment_size=2)
    FOOTWEAR_COUNTS_START = AddressData(address=0x0F6A50, segment_size=1)
    FOOTWEAR_COUNTS_END = AddressData(address=0x0F6A4E, segment_size=1)
    FOOTWEAR_SEGMENTS = 112

    # Accessories (Bag)
    ACCESSORIES_TYPE_START = AddressData(address=0x0F6AC0, segment_size=2)
    ACCESSORIES_TYPE_END = AddressData(address=0x0F6B3E, segment_size=2)
    ACCESSORIES_COUNTS_START = AddressData(address=0x0F6B40, segment_size=1)
    ACCESSORIES_COUNTS_END = AddressData(address=0x0F6B7F, segment_size=1)
    ACCESSORIES_SEGMENTS = 64

    # Important Items (Bag)
    IMPORTANT_ITEMS_TYPE_START = AddressData(address=0x0F6BEC, segment_size=2)
    IMPORTANT_ITEMS_TYPE_END = AddressData(address=0x0F6CA6, segment_size=2)
    IMPORTANT_ITEMS_COUNTS_START = AddressData(address=0x0F6CA8, segment_size=1)
    IMPORTANT_ITEMS_COUNTS_END = AddressData(address=0x0F6D05, segment_size=1)
    IMPORTANT_ITEMS_SEGMENTS = 94

    DQVC_MESSAGE = AddressData(address=0x0F9358, segment_size=2)
