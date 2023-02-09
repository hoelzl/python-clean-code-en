from collections.abc import Collection
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import sys

from .location import Location, LocationDescriptions


LocationDict = Dict[str, Location]


@dataclass
class World:
    locations: LocationDict
    initial_location_name: str
    connections: Dict[str, LocationDict] = field(default_factory=dict)

    def __getitem__(self, location_name: str):
        """Return the connected location in direction `location_name`.

        >>> world = World.from_location_descriptions([{"name": "A"}, {"name": "B"}])
        >>> world["A"]
        Location(name='A')
        >>> world["B"]
        Location(name='B')
        >>> world["C"]
        Traceback (most recent call last):
        ...
        KeyError: 'C'
        """
        return self.locations[location_name]

    @classmethod
    def from_location_descriptions(
        cls, location_descriptions: LocationDescriptions
    ) -> "World":
        """Create a World from a description of its locations.

        >>> World.from_location_descriptions(
        ...         [{"name": "A", "connections": {"east": "B"}},
        ...          {"name": "B", "connections": {"west": "A"}}])
        World(locations={'A': Location(name='A'), 'B': Location(name='B')},
              initial_location_name='A',
              connections={'A': {'east': Location(name='B')},
                           'B': {'west': Location(name='A')}})
        """
        result = cls(
            locations=(_create_locations(location_descriptions)),
            initial_location_name=location_descriptions[0]["name"],
        )
        _build_connections_for_all_locations(location_descriptions, result)
        return result

    def connection(self, location: Location, direction: str) -> Optional[Location]:
        """Return the connected location in a given direction, or `None`."""
        return self.connections[location.name].get(direction)


def _create_locations(location_descriptions: LocationDescriptions) -> LocationDict:
    """Create a location dictionary from descriptions.

    >>> _create_locations(
    ...         [{"name": "A", "connections": {"east": "B"}},
    ...          {"name": "B", "connections": {"west": "A"}}])
    {'A': Location(name='A'), 'B': Location(name='B')}
    """
    return {
        location_description["name"]: Location(location_description["name"])
        for location_description in location_descriptions
    }


def _build_connections_for_all_locations(location_descriptions, result):
    for ld in location_descriptions:
        result.connections[ld["name"]] = {
            direction: result[loc_name]
            for direction, loc_name in ld.get("connections", {}).items()
        }
