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

        region_stornway = Region("Stornway / Zere", self.player, self.multiworld)
        region_coffinwell = Region("Coffinwell", self.player, self.multiworld)
        region_alltrades = Region("Alltrades Abbey / Porth Llaffan / Observatory (After Attack)", self.player, self.multiworld)
        region_bloomingdale_zere = Region("A new continent (Slurry Quay / Dourbridge / Zere Rocks / Bloomingdale)", self.player, self.multiworld)
        region_ship_places = Region("A new World (Gleeba, Batsureg, Swinedimpels (Wormwood Creek))", self.player, self.multiworld)
        region_bowhole = Region("Wormwood Creek / Bowhole", self.player, self.multiworld)
        region_upover = Region("Upover / Magmaroo", self.player, self.multiworld)
        region_goretress = Region("Goretress", self.player, self.multiworld)
        region_gittingham_palace = Region("Gittingham Palace", self.player, self.multiworld)
        region_realm_mighty = Region("Realm of the Mighty", self.player, self.multiworld)

        main_region.connect(connecting_region=region_stornway, rule=lambda state: state.has(item="Inny", player=self.player, count=1))
        region_stornway.connect(connecting_region=region_coffinwell, )  # Check for game chapter
        region_coffinwell.connect(connecting_region=region_alltrades, )  # Has returned to the Observatory, perhaps count benevolessence?
        region_alltrades.connect(connecting_region=region_bloomingdale_zere, rule=lambda state: state.has(item="Fygg", player=self.player, count=1))
        region_bloomingdale_zere.connect(connecting_region=region_ship_places, )  # Check if has unlocked ship
        region_ship_places.connect(connecting_region=region_bowhole, rule=lambda state: state.has(item="Serene necklace", player=self.player, count=1))  # Bowhole has been unlocked / Seren Necklace?
        region_bowhole.connect(connecting_region=region_upover, rule=lambda state: state.has(item="Wyrmlight bow", player=self.player, count=1))
        region_upover.connect(connecting_region=region_goretress, )  # When battle of Greygnarl vs Barbarus happens
        region_goretress.connect(connecting_region=region_gittingham_palace, rule=lambda state: state.has(item="Ultimate key", player=self.player, count=1))  # After boss has been defeated
        region_gittingham_palace.connect(connecting_region=region_realm_mighty, )  # After "killed" by Corvus, perhaps game chapter

        self.multiworld.regions.append(region_stornway)
        self.multiworld.regions.append(region_coffinwell)
        self.multiworld.regions.append(region_alltrades)
        self.multiworld.regions.append(region_bloomingdale_zere)
        self.multiworld.regions.append(region_ship_places)
        self.multiworld.regions.append(region_bowhole)
        self.multiworld.regions.append(region_upover)
        self.multiworld.regions.append(region_goretress)
        self.multiworld.regions.append(region_gittingham_palace)
        self.multiworld.regions.append(region_realm_mighty)

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.item_helper.get_filler_item_names())
