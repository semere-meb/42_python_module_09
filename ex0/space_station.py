#! /usr/bin/env python3

from datetime import datetime
from pydantic import Field, BaseModel, ValidationError
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print()
    print("Space Station Data Validation")
    print("=" * 30)
    print()

    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.now(),
        is_operational=True,
    )

    print("Valid station created:")
    print("ID:", station.station_id)
    print("Name:", station.name)
    print("Name:", station.crew_size, "people")
    print(f"Name: {station.power_level}%")
    print(f"Name: {station.oxygen_level}%")
    print("Name:",
          "Operational" if station.is_operational else "Non-operational")

    print()
    print("=" * 30)

    try:
        SpaceStation(
          **{
            "station_id": "TOOLONG123456",
            "name": "Test Station",
            "crew_size": 25,
            "power_level": 85.0,
            "oxygen_level": 92.0,
            "last_maintenance": "2024-01-15T10:30:00",
            "is_operational": True
          },
        )
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["loc"], ": ", err["msg"])


if __name__ == "__main__":
    main()
