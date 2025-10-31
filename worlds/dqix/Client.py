from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class DQIXClient(BizHawkClient):
    game = "Dragon Quest IX"
    system = "NDS"

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

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        try:
            await self.location_check(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def location_check(self, ctx: "BizHawkClientContext"):
        money_value = int.from_bytes((await bizhawk.read(ctx=ctx.bizhawk_ctx, read_list=[(0x0F6D48, 4, "Main RAM")]))[0], "little")
        if money_value != self.current_money:
            print("Money on Hand has changed to: " + str(money_value))
            self.current_money = money_value
