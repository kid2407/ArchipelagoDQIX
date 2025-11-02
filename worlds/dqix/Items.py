import json
import pkgutil
from typing import Dict, NamedTuple

from BaseClasses import ItemClassification


class ItemData(NamedTuple):
    name: str
    code: int
    item_type: str
    classification: ItemClassification


class DQIXItems:
    _item_table: Dict[str, ItemData] = {}

    def _parse_item_data(self):
        file = pkgutil.get_data(__name__, "data/items.json").decode("utf-8")
        items = json.loads(file)

        self.progression_items = {name: ItemData(name, code, "progression", ItemClassification.progression) for name, code in items["progression"].items()}
        self.useful_items = {name: ItemData(name, code, "useful", ItemClassification.useful) for name, code in items["useful"].items()}
        self.filler_items = {name: ItemData(name, code, "extra", ItemClassification.filler) for name, code in items["filler"].items()}

        final_item_table = {}
        final_item_table.update(self.progression_items)
        final_item_table.update(self.useful_items)
        final_item_table.update(self.filler_items)

        self._item_table = final_item_table

    def _get_item_table(self):
        if not self._item_table:
            self._parse_item_data()
        return self._item_table

    def get_items(self) -> Dict[str, int]:
        return {name: item.code for name, item in self._get_item_table().items()}

    def get_item_type(self, name: str):
        return self._get_item_table()[name].item_type

    def is_progression(self, name: str) -> bool:
        return name in self.progression_items

    def is_useful(self, name: str) -> bool:
        return name in self.useful_items
