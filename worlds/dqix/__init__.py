import logging
from typing import Optional

from BaseClasses import Tutorial, Item, ItemClassification, Location, Region
from ..AutoWorld import World, WebWorld
from .Client import DQIXClient
from .Items import DQIXItems
from .Locations import DQIXLocations


class DQIXItem(Item):
    game = "Dragon Quest IX"
    item_type: str

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int, item_type: str):
        super(DQIXItem, self).__init__(name, classification, code, player)
        self.item_type = item_type


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
    origin_region_name = "Angel Falls"
    web = DragonQuestIXWeb()

    items = DQIXItems()
    locations = DQIXLocations()

    item_name_to_id = items.get_items()
    location_name_to_id = locations.get_locations()

    location_count: int = len(location_name_to_id)

    def create_item(self, name: str) -> "DQIXItem":
        return DQIXItem(
            name,
            ItemClassification.progression if self.items.is_progression(name) else ItemClassification.useful if self.items.is_useful(name) else ItemClassification.filler,
            self.item_name_to_id[name],
            self.player,
            self.items.get_item_type(name)
        )

    def create_items(self) -> None:
        items = [self.create_item(name) for name in self.item_id_to_name.values()]
        items += [self.create_item("500 Gold") for _ in range(self.location_count - len(items))]

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        main_region = Region(self.origin_region_name, self.player, self.multiworld)
        main_region.add_locations(self.location_name_to_id, DQIXLocation)
        self.multiworld.regions.append(main_region)
