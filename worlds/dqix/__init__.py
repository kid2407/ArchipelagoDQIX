from typing import Optional

from BaseClasses import Tutorial, Item, ItemClassification, Location, Region
from ..AutoWorld import World, WebWorld
from .Items import DQIXItems
from .Client import DQIXClient
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

    location_helper = DQIXLocations()
    item_helper = DQIXItems()

    location_name_to_id = location_helper.get_locations()
    item_name_to_id = item_helper.get_items()

    def create_item(self, name: str) -> "DQIXItem":
        return DQIXItem(
            name,
            ItemClassification.progression if self.item_helper.is_progression(name) else ItemClassification.useful if self.item_helper.is_useful(name) else ItemClassification.filler,
            self.item_name_to_id[name],
            self.player,
            self.item_helper.get_item_type(name)
        )

    def create_items(self) -> None:
        progression_item_names = {k for k in self.item_name_to_id.keys() if self.item_helper.is_progression(k)}
        items = [self.create_item(name) for name in progression_item_names]
        remaining_count_until_almost_full = (round(len(self.location_name_to_id) * 0.9) - len(items))
        items += [self.create_item(useful_item) for useful_item in self.random.choices(population=list(self.item_helper.useful_items.keys()), k=remaining_count_until_almost_full)]

        items += [self.create_item(self.get_filler_item_name()) for _ in range(len(self.location_name_to_id) - len(items))]

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        main_region = Region(self.origin_region_name, self.player, self.multiworld)
        main_region.add_locations(self.location_name_to_id, DQIXLocation)
        self.multiworld.regions.append(main_region)

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.item_helper.get_filler_item_names())
