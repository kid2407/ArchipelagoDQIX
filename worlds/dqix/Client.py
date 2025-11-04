import logging
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from NetUtils import NetworkItem
from worlds._bizhawk.client import BizHawkClient
from worlds.dqix import DQIXItems
from worlds.dqix.Items import ItemType

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class DQIXClient(BizHawkClient):
    game = "Dragon Quest IX"
    system = "NDS"
    last_known_index = None

    def __init__(self):
        self.current_money = None
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 12, "ROM")]))[0]).decode("ascii")
            if rom_name != "DRAGONQUEST9":
                return False  # Not a MYGAME ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        # This is a MYGAME ROM
        ctx.game = self.game
        ctx.want_slot_data = True
        ctx.items_handling = 0b111

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot_data is None:
            return

        try:
            await self.location_check(ctx)
            await self.received_items_check(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def location_check(self, ctx: "BizHawkClientContext"):
        money_value = int.from_bytes((await bizhawk.read(ctx=ctx.bizhawk_ctx, read_list=[(0x0F6D48, 4, "Main RAM")]))[0], "little")
        if money_value != self.current_money:
            logging.info("Money on Hand has changed to: " + str(money_value))
            self.current_money = money_value

    async def received_items_check(self, ctx: "BizHawkClientContext"):
        network_item: NetworkItem
        for index, network_item in enumerate(ctx.items_received):
            if self.last_known_index is None or self.last_known_index < index:
                self.last_known_index = index
                logging.info("Received Item: ID = {0} and Location = {1} from Player = {2}".format(network_item.item, network_item.location, network_item.player))
                await bizhawk.set_message_interval(5)
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Received Item with ID {network_item.item}")
                await self.grant_item(ctx=ctx, item_id=network_item.item)
                # TODO actually grant the received item, depending on what it is, e.g. gold is easy
                # TODO save the last item index in a save file or save state

    def determine_item_type(self, item_id: int):
        if 12000 <= item_id < 22000:
            return ItemType.EQUIPMENT
        elif 22000 <= item_id < 23000:
            return ItemType.IMPORTANT_ITEM if id in DQIXItems.IMPORTANT_ITEM_IDS else ItemType.COMMON_ITEM
        elif 100000 <= item_id < 100010:
            return ItemType.GOLD
        elif 100010 <= item_id < 100020:
            return ItemType.EXPERIENCE
        return None

    async def read_value_as_int_from_ram(self, ctx: "BizHawkClientContext", address: int, size: int):
        return int.from_bytes((await bizhawk.read(ctx=ctx.bizhawk_ctx, read_list=[(address, size, "Main RAM")]))[0], "little")

    async def write_value_as_int_to_ram(self, ctx: "BizHawkClientContext", address: int, size: int, value: int):
        await bizhawk.write(ctx=ctx.bizhawk_ctx, write_list=[(address, int.to_bytes(value, size, "little"), "Main RAM")])

    async def grant_item(self, ctx: "BizHawkClientContext", item_id: int):
        item_type = self.determine_item_type(item_id)
        match item_type:
            case ItemType.GOLD:
                current_gold = await self.read_value_as_int_from_ram(ctx=ctx, address=0x0F6D48, size=4)
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
                await self.write_value_as_int_to_ram(ctx=ctx, address=0x0F6D48, size=4, value=current_gold + gold_gained)
