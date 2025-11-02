import json
import pkgutil
from typing import Dict


class DQIXLocations:
    _location_table: Dict[str, int] = {}

    def _parse_location_data(self):
        file = pkgutil.get_data(__name__, "data/locations.json").decode("utf-8")
        locations = json.loads(file)

        self._location_table = locations

    def _get_location_table(self):
        if not self._location_table:
            self._parse_location_data()
        return self._location_table

    def get_locations(self):
        return self._get_location_table()
