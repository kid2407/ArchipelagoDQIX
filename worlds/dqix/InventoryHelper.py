import logging
from enum import Enum
from typing import TYPE_CHECKING

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
                await self.give_player_item(item_start_address=DQIXConstants.IMPORTANT_ITEMS_TYPE_OFFSET.address, amount_start_address=DQIXConstants.IMPORTANT_ITEMS_COUNTS_OFFSET.address, segment_count=DQIXConstants.IMPORTANT_ITEMS_SEGMENTS,
                                            item_id=item_id)
            case ItemType.COMMON_ITEM:
                await self.give_player_item(item_start_address=DQIXConstants.COMMON_ITEMS_TYPE_OFFSET.address, amount_start_address=DQIXConstants.COMMON_ITEMS_COUNTS_OFFSET.address, segment_count=DQIXConstants.COMMON_ITEMS_SEGMENTS, item_id=item_id)
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

    async def grant_equipment(self, item_id: int):
        equipment_type = self.determine_equipment_type(item_id)

        match equipment_type:
            case EquipmentType.WEAPONS:
                await self.give_player_item(DQIXConstants.WEAPONS_TYPE_OFFSET.address, DQIXConstants.WEAPONS_COUNTS_OFFSET.address, DQIXConstants.WEAPONS_SEGMENTS, item_id)
            case EquipmentType.SHIELDS:
                await self.give_player_item(DQIXConstants.SHIELDS_TYPE_OFFSET.address, DQIXConstants.SHIELDS_COUNTS_OFFSET.address, DQIXConstants.SHIELDS_SEGMENTS, item_id)
            case EquipmentType.HEADWEAR:
                await self.give_player_item(DQIXConstants.HEADWEAR_TYPE_OFFSET.address, DQIXConstants.HEADWEAR_COUNTS_OFFSET.address, DQIXConstants.HEADWEAR_SEGMENTS, item_id)
            case EquipmentType.TORSO:
                await self.give_player_item(DQIXConstants.TORSO_TYPE_OFFSET.address, DQIXConstants.TORSO_COUNTS_OFFSET.address, DQIXConstants.TORSO_SEGMENTS, item_id)
            case EquipmentType.ARMS:
                await self.give_player_item(DQIXConstants.ARMS_TYPE_OFFSET.address, DQIXConstants.ARMS_COUNTS_OFFSET.address, DQIXConstants.ARMS_SEGMENTS, item_id)
            case EquipmentType.LEGS:
                await self.give_player_item(DQIXConstants.LEGS_TYPE_OFFSET.address, DQIXConstants.LEGS_COUNTS_OFFSET.address, DQIXConstants.LEGS_SEGMENTS, item_id)
            case EquipmentType.FOOTWEAR:
                await self.give_player_item(DQIXConstants.FOOTWEAR_TYPE_OFFSET.address, DQIXConstants.FOOTWEAR_COUNTS_OFFSET.address, DQIXConstants.FOOTWEAR_SEGMENTS, item_id)
            case EquipmentType.ACCESSORIES:
                await self.give_player_item(DQIXConstants.ACCESSORIES_TYPE_OFFSET.address, DQIXConstants.ACCESSORIES_COUNTS_OFFSET.address, DQIXConstants.ACCESSORIES_SEGMENTS, item_id)
            case None:
                logging.warning("Uh-oh, could not determine the equipment type for equipment with ID = {0}. This should not happen, please report this error to the author.".format(item_id))

    async def give_player_item(self, item_start_address: int, amount_start_address: int, segment_count: int, item_id: int):
        item_inventory = await self.read_segments_as_ints_from_ram(item_start_address, segment_count, 2)

        try:
            target_slot = item_inventory.index(item_id)
            existing_slot = True
        except ValueError:
            try:
                target_slot = item_inventory.index(65535)
                existing_slot = False
            except ValueError:
                logging.warning("Cannot add item \"{}\": No empty slot in inventory found!".format(item_id))
                return

        item_address = hex(item_start_address + 2 * target_slot)
        amount_address = hex(amount_start_address + target_slot)

        if existing_slot:
            old_value = await self.read_int_from_ram(address=amount_address, size=1)
            await self.write_int_to_ram(address=amount_address, size=1, value=min(old_value + 1, 99))
        else:
            await self.write_int_to_ram(address=item_address, size=2, value=item_id)
            await self.write_int_to_ram(address=amount_address, size=1, value=1)
