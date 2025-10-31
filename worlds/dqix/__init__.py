from BaseClasses import Tutorial, Item, ItemClassification, Location, Region
from worlds.AutoWorld import World, WebWorld
from .Client import DQIXClient


class DQIXItem(Item):
    game = "Dragon Quest IX"


class DQIXLocation(Location):
    game = "Dragon Quest IX"


class DragonQuestIXWeb(WebWorld):
    game_info_languages = ["en"]
    theme = "ocean"
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
    required_client_version = (0, 6, 3)
    web = DragonQuestIXWeb()

    item_name_to_id = {"Fygg": 123456}
    location_name_to_id = {"start": 1}

    main_locations = {"start": 1}

    def create_item(self, name: str) -> "DQIXItem":
        print("Creating Item: " + name)

        return DQIXItem("Fygg", ItemClassification.progression, 1, self.player)

    def create_items(self) -> None:
        items = [DQIXItem("Fygg", ItemClassification.progression, 123456, self.player)]

        self.multiworld.itempool += items

    origin_region_name = "Angel Falls"

    def create_regions(self) -> None:
        main_region = Region(self.origin_region_name, self.player, self.multiworld)
        main_region.add_locations(self.main_locations, DQIXLocation)
        self.multiworld.regions.append(main_region)
