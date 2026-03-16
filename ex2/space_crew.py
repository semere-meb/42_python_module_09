#! /usr/bin/env python3

from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specalization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    misssion_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_model(self):
        errors = []

        if not self.mission_id.startswith("M"):
            errors.append("Incorrect mission id")
        ranks = [member.rank for member in self.crew]
        if not Rank.captain not in ranks or Rank.commander not in ranks:
            errors.append("Mission must have a commander or a captain")
        experienced = [
            member for member in self.crew
            if member.years_experience >= 5
        ]
        if self.duration_days > 365 and len(experienced) < len(self.crew):
            errors.append("Inexperienced crew for this mission")
        if not all(member.is_active for member in self.crew):
            errors.append("Mission must not have inactive crew members")

        if errors:
            raise ValueError(errors)

        return self


def main() -> None:
    print("\nSpace Mission Crew Validation")
    print("=" * 30)
    print()

    mission = SpaceMission(
        mission_id="M2024",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        duration_days=900,
        budget_millions=2500,
        launch_date=datetime.now(),
        crew=[
            CrewMember(
                member_id="sco",
                name="Sarah Conor",
                rank=Rank.commander,
                age=50,
                specalization="Mission Command",
                years_experience=20,
            ),
            CrewMember(
                member_id="sco",
                name="John Smith",
                rank=Rank.lieutenant,
                age=40,
                specalization="Navigation",
                years_experience=15,
            ),
            CrewMember(
                member_id="ajo",
                name="Alice Johnson",
                rank=Rank.officer,
                age=32,
                specalization="Engineering",
                years_experience=20,
            ),
        ],
    )
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value})- {member.specalization}")

    print()
    print("=" * 30)

    try:
        SpaceMission(
            mission_id="M2024",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            budget_millions=2500,
            launch_date=datetime.now(),
            crew=[
                CrewMember(
                    member_id="sco",
                    name="Sarah Conor",
                    rank=Rank.lieutenant,
                    age=50,
                    specalization="Mission Command",
                    years_experience=2,
                ),
                CrewMember(
                    member_id="sco",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=40,
                    specalization="Navigation",
                    years_experience=3,
                ),
                CrewMember(
                    member_id="ajo",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=32,
                    specalization="Engineering",
                    years_experience=20,
                ),
            ],
        )
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
