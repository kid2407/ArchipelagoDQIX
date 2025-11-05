import logging
from enum import Enum
from typing import TYPE_CHECKING, List

import worlds._bizhawk as bizhawk
from worlds.dqix.Constants import DQIXConstants
from worlds.dqix.Items import ItemType, DQIXItems

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class EquipmentType(Enum):
    WEAPONS = "WEAPONS"
    SHIELDS = "SHIELDS"
    TORSO = "TORSO"
    LEGS = "LEGS"
    HEADWEAR = "HEADWEAR"
    ARMS = "ARMS"
    FOOTWEAR = "FOOTWEAR"
    ACCESSORIES = "ACCESSORIES"


class InventoryHelper:
    def __init__(self, ctx: "BizHawkClientContext"):
        self.ctx = ctx

    @staticmethod
    def determine_item_type(item_id: int):
        if 12000 <= item_id < 22000:
            return ItemType.EQUIPMENT
        elif 22000 <= item_id < 23000:
            return ItemType.IMPORTANT_ITEM if item_id in DQIXItems.IMPORTANT_ITEM_IDS else ItemType.COMMON_ITEM
        elif 100000 <= item_id < 100010:
            return ItemType.GOLD
        elif 100010 <= item_id < 100020:
            return ItemType.EXPERIENCE
        return None

    @staticmethod
    def determine_equipment_type(item_id: int):
        if 19050 <= item_id <= 2091822:
            return EquipmentType.WEAPONS
        elif 21000 <= item_id < 22000:
            return EquipmentType.SHIELDS
        elif 12100 <= item_id < 13000:
            return EquipmentType.HEADWEAR
        elif 13000 <= item_id < 14000:
            return EquipmentType.TORSO
        elif 15000 <= item_id < 15300:
            return EquipmentType.ARMS
        elif 16000 <= item_id < 16400:
            return EquipmentType.LEGS
        elif 17000 <= item_id < 17500:
            return EquipmentType.FOOTWEAR
        elif 18000 <= item_id < 18055:
            return EquipmentType.ACCESSORIES
        return None

    async def read_int_from_ram(self, address: int | str, size: int):
        address = int(address, 16) if isinstance(address, str) else address
        return int.from_bytes((await bizhawk.read(ctx=self.ctx.bizhawk_ctx, read_list=[(address, size, "Main RAM")]))[0], "little")

    async def write_int_to_ram(self, address: int | str, size: int, value: int):
        address = int(address, 16) if isinstance(address, str) else address
        await bizhawk.write(ctx=self.ctx.bizhawk_ctx, write_list=[(address, int.to_bytes(value, size, "little"), "Main RAM")])

    async def read_segments_as_ints_from_ram(self, address: int | str, segment_count: int, segment_size: int = 1):
        address = int(address, 16) if isinstance(address, str) else address
        read_bytes = (await bizhawk.read(ctx=self.ctx.bizhawk_ctx, read_list=[(address, segment_size * segment_count, "Main RAM")]))[0]
        return [int.from_bytes(read_bytes[segment * segment_size:(segment * segment_size + segment_size)], "little") for segment in range(segment_count)]

    async def grant_received_item(self, item_id: int):
        item_type = self.determine_item_type(item_id)

        match item_type:
            case ItemType.GOLD:
                await self.grant_gold(item_id=item_id)
            case ItemType.EXPERIENCE:
                await self.grant_experience(item_id=item_id)
            case ItemType.IMPORTANT_ITEM:
                await self.grant_important_item(item_id=item_id)
            case ItemType.COMMON_ITEM:
                await self.grant_common_item(item_id=item_id)
            case ItemType.EQUIPMENT:
                await self.grant_equipment(item_id=item_id)
            case None:
                logging.warning("Uh-oh, could not determine the item type for item with ID = {0}. This should not happen, please report this error to the author.".format(item_id))

    async def grant_gold(self, item_id: int):
        current_gold = await self.read_int_from_ram(address=DQIXConstants.GOLD_AT_HAND.address, size=DQIXConstants.GOLD_AT_HAND.segment_size)
        gold_gained = 0
        match item_id:
            case 100000:
                gold_gained = 50
            case 100001:
                gold_gained = 500
            case 100002:
                gold_gained = 5000
            case 100003:
                gold_gained = 50000
        await self.write_int_to_ram(address=DQIXConstants.GOLD_AT_HAND.address, size=DQIXConstants.GOLD_AT_HAND.segment_size, value=min(max(current_gold + gold_gained, 0), 999999999))

    async def grant_experience(self, item_id: int):
        # TODO Get class and EXP for the current vocations of the group
        # TODO Then Add experience per character in the party
        # TODO Check if it breaks anything when modifying EXP like this
        exp_gained = 0
        match item_id:
            case 100010:
                exp_gained = 50
            case 100011:
                exp_gained = 500
            case 100012:
                exp_gained = 5000
            case 100013:
                exp_gained = 50000

    async def grant_important_item(self, item_id: int):
        important_item_inventory = await self.read_segments_as_ints_from_ram(
            DQIXConstants.IMPORTANT_ITEMS_TYPE_START.address,
            DQIXConstants.IMPORTANT_ITEMS_SEGMENTS,
            DQIXConstants.IMPORTANT_ITEMS_TYPE_START.segment_size
        )

        try:
            target_slot = important_item_inventory.index(65535)
            existing_slot = True
        except ValueError:
            existing_slot = False
            try:
                target_slot = important_item_inventory.index(65535)
            except ValueError:
                logging.warning("Cannot add common item \"{}\": No empty slot in inventory found!".format(item_id))
                return

        target_address = hex(DQIXConstants.IMPORTANT_ITEMS_TYPE_START.address + DQIXConstants.IMPORTANT_ITEMS_TYPE_START.segment_size * target_slot)
        amount_address = hex(DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.address + DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.segment_size * target_slot)

        if existing_slot:
            old_value = await self.read_int_from_ram(address=DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.address + DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.segment_size * target_slot, size=DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.segment_size)
            await self.write_int_to_ram(address=amount_address, size=DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.segment_size, value=min(old_value + 1, 99))
        else:
            await self.write_int_to_ram(address=target_address, size=DQIXConstants.IMPORTANT_ITEMS_TYPE_START.segment_size, value=item_id)
            await self.write_int_to_ram(address=amount_address, size=DQIXConstants.IMPORTANT_ITEMS_COUNTS_START.segment_size, value=1)

    async def grant_common_item(self, item_id: int):
        common_item_inventory = await self.read_segments_as_ints_from_ram(
            DQIXConstants.COMMON_ITEMS_TYPE_START.address,
            DQIXConstants.COMMON_ITEMS_SEGMENTS,
            DQIXConstants.COMMON_ITEMS_TYPE_START.segment_size
        )

        try:
            target_slot = common_item_inventory.index(item_id)
            existing_slot = True
        except ValueError:
            try:
                target_slot = common_item_inventory.index(65535)
                existing_slot = False
            except ValueError:
                logging.warning("Cannot add common item \"{}\": No empty slot in inventory found!".format(item_id))
                return

        target_address = hex(DQIXConstants.COMMON_ITEMS_TYPE_START.address + DQIXConstants.COMMON_ITEMS_TYPE_START.segment_size * target_slot)

        amount_address = hex(DQIXConstants.COMMON_ITEMS_COUNTS_START.address + DQIXConstants.COMMON_ITEMS_COUNTS_START.segment_size * target_slot)
        if existing_slot:
            old_value = await self.read_int_from_ram(address=DQIXConstants.COMMON_ITEMS_COUNTS_START.address + DQIXConstants.COMMON_ITEMS_COUNTS_START.segment_size * target_slot, size=DQIXConstants.COMMON_ITEMS_COUNTS_START.segment_size)
            await self.write_int_to_ram(address=amount_address, size=DQIXConstants.COMMON_ITEMS_COUNTS_START.segment_size, value=min(old_value + 1, 99))
        else:
            await self.write_int_to_ram(address=target_address, size=DQIXConstants.COMMON_ITEMS_TYPE_START.segment_size, value=item_id)
            await self.write_int_to_ram(address=amount_address, size=DQIXConstants.COMMON_ITEMS_COUNTS_START.segment_size, value=1)

    async def grant_equipment(self, item_id: int):
        equipment_type = self.determine_equipment_type(item_id)
