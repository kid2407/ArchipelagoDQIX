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

    async def read_ints_from_ram(self, addresses: List[int | str], size: int) -> List[int]:
        data = await bizhawk.read(ctx=self.ctx.bizhawk_ctx, read_list=[(int(address, 16) if isinstance(address, str) else address, size, "Main RAM") for address in addresses])
        return [int.from_bytes(found_bytes, "little") for found_bytes in data]

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
                await self.give_player_item(item_offset=DQIXConstants.IMPORTANT_ITEMS_TYPE_OFFSET, amount_offset=DQIXConstants.IMPORTANT_ITEMS_COUNTS_OFFSET,
                                            segment_count=DQIXConstants.IMPORTANT_ITEMS_SEGMENTS, item_id=item_id)
            case ItemType.COMMON_ITEM:
                await self.give_player_item(item_offset=DQIXConstants.COMMON_ITEMS_TYPE_OFFSET, amount_offset=DQIXConstants.COMMON_ITEMS_COUNTS_OFFSET,
                                            segment_count=DQIXConstants.COMMON_ITEMS_SEGMENTS, item_id=item_id)
            case ItemType.EQUIPMENT:
                await self.grant_equipment(item_id=item_id)
            case None:
                logging.warning("Uh-oh, could not determine the item type for item with ID = {0}. This should not happen, please report this error to the author.".format(item_id))

    async def grant_gold(self, item_id: int):
        current_gold = await self.read_int_from_ram(address=DQIXConstants.GOLD_AT_HAND, size=DQIXConstants.GOLD_VALUE_SIZE)
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
        await self.write_int_to_ram(address=DQIXConstants.GOLD_AT_HAND, size=DQIXConstants.GOLD_VALUE_SIZE, value=min(max(current_gold + gold_gained, 0), 999999999))

    async def grant_experience(self, item_id: int):
        # TODO Check if it breaks anything when modifying EXP like this
        exp_gained = 0
        match item_id:
            case 100010:
                exp_gained = 50
            case 100011:
                exp_gained = 4096
            case 100012:
                exp_gained = 12288
            case 100013:
                exp_gained = 40200

        if exp_gained > 0:
            character_vocations = await self.read_ints_from_ram([
                DQIXConstants.CHAR_1_CURRENT_VOCATION,
                DQIXConstants.CHAR_2_CURRENT_VOCATION,
                DQIXConstants.CHAR_3_CURRENT_VOCATION,
                DQIXConstants.CHAR_4_CURRENT_VOCATION
            ], 4)

            await self.give_character_experience(current_vocation=character_vocations[0], experience_offset=DQIXConstants.CHAR_1_VOCATION_EXP_OFFSET, earned_experience=exp_gained)
            await self.give_character_experience(current_vocation=character_vocations[1], experience_offset=DQIXConstants.CHAR_2_VOCATION_EXP_OFFSET, earned_experience=exp_gained)
            await self.give_character_experience(current_vocation=character_vocations[2], experience_offset=DQIXConstants.CHAR_3_VOCATION_EXP_OFFSET, earned_experience=exp_gained)
            await self.give_character_experience(current_vocation=character_vocations[3], experience_offset=DQIXConstants.CHAR_4_VOCATION_EXP_OFFSET, earned_experience=exp_gained)

    async def grant_equipment(self, item_id: int):
        equipment_type = self.determine_equipment_type(item_id)

        match equipment_type:
            case EquipmentType.WEAPONS:
                await self.give_player_item(DQIXConstants.WEAPONS_TYPE_OFFSET, DQIXConstants.WEAPONS_COUNTS_OFFSET, DQIXConstants.WEAPONS_SEGMENTS, item_id)
            case EquipmentType.SHIELDS:
                await self.give_player_item(DQIXConstants.SHIELDS_TYPE_OFFSET, DQIXConstants.SHIELDS_COUNTS_OFFSET, DQIXConstants.SHIELDS_SEGMENTS, item_id)
            case EquipmentType.HEADWEAR:
                await self.give_player_item(DQIXConstants.HEADWEAR_TYPE_OFFSET, DQIXConstants.HEADWEAR_COUNTS_OFFSET, DQIXConstants.HEADWEAR_SEGMENTS, item_id)
            case EquipmentType.TORSO:
                await self.give_player_item(DQIXConstants.TORSO_TYPE_OFFSET, DQIXConstants.TORSO_COUNTS_OFFSET, DQIXConstants.TORSO_SEGMENTS, item_id)
            case EquipmentType.ARMS:
                await self.give_player_item(DQIXConstants.ARMS_TYPE_OFFSET, DQIXConstants.ARMS_COUNTS_OFFSET, DQIXConstants.ARMS_SEGMENTS, item_id)
            case EquipmentType.LEGS:
                await self.give_player_item(DQIXConstants.LEGS_TYPE_OFFSET, DQIXConstants.LEGS_COUNTS_OFFSET, DQIXConstants.LEGS_SEGMENTS, item_id)
            case EquipmentType.FOOTWEAR:
                await self.give_player_item(DQIXConstants.FOOTWEAR_TYPE_OFFSET, DQIXConstants.FOOTWEAR_COUNTS_OFFSET, DQIXConstants.FOOTWEAR_SEGMENTS, item_id)
            case EquipmentType.ACCESSORIES:
                await self.give_player_item(DQIXConstants.ACCESSORIES_TYPE_OFFSET, DQIXConstants.ACCESSORIES_COUNTS_OFFSET, DQIXConstants.ACCESSORIES_SEGMENTS, item_id)
            case None:
                logging.warning("Uh-oh, could not determine the equipment type for equipment with ID = {0}. This should not happen, please report this error to the author.".format(item_id))

    async def give_player_item(self, item_offset: int, amount_offset: int, segment_count: int, item_id: int):
        item_inventory = await self.read_segments_as_ints_from_ram(item_offset, segment_count, DQIXConstants.ITEM_TYPE_SIZE)

        try:
            target_slot = item_inventory.index(item_id)
            existing_slot = True
        except ValueError:
            try:
                target_slot = item_inventory.index(DQIXConstants.ITEM_DATA_NO_ITEM)
                existing_slot = False
            except ValueError:
                logging.warning("Cannot add item \"{}\": No empty slot in inventory found!".format(item_id))
                return

        item_address = hex(item_offset + 2 * target_slot)
        amount_address = hex(amount_offset + target_slot)

        if existing_slot:
            old_value = await self.read_int_from_ram(address=amount_address, size=DQIXConstants.ITEM_AMOUNT_SIZE)
            await self.write_int_to_ram(address=amount_address, size=DQIXConstants.ITEM_AMOUNT_SIZE, value=min(old_value + 1, 99))
        else:
            await self.write_int_to_ram(address=item_address, size=DQIXConstants.ITEM_TYPE_SIZE, value=item_id)
            await self.write_int_to_ram(address=amount_address, size=DQIXConstants.ITEM_AMOUNT_SIZE, value=1)

    async def give_character_experience(self, current_vocation: int, experience_offset: int, earned_experience: int):
        logging.warning("Current vocation: " + str(current_vocation))
        logging.warning("Exp Offset: " + hex(experience_offset))
        if current_vocation == 0:
            return

        target_address = experience_offset + (current_vocation - 1) * 4
        current_exp = await self.read_int_from_ram(target_address, 4)
        logging.warning("Current exp: " + str(current_exp))
        await self.write_int_to_ram(target_address, 4, current_exp + earned_experience)
