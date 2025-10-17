from BaseClasses import Tutorial, Item, ItemClassification
from worlds.AutoWorld import World, WebWorld


class DragonQuestIXWeb(WebWorld):
    game_info_languages = ["en"]
    setup_en = Tutorial(
        tutorial_name="Setup the Game",
        description="This shows you how to setup DQIX properly",
        language="en",
        file_name="setup_en.md",
        link="setup/en",
        authors=["kid2407"]
    )

    tutorials = [setup_en]


class DragonQuestIX(World):
    game = "Dragon Quest IX"
    required_client_version = (0, 6, 4)
    web = DragonQuestIXWeb()

    item_name_to_id = {"fygg": 1}
    location_name_to_id = {"start": 1}

    def create_item(self, name: str) -> "Item":
        return Item("fygg", ItemClassification.progression, 1, 1)
