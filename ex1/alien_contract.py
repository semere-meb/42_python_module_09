#! /usr/bin/env python3

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telephatic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_model(self):
        errors = []

        if not self.contact_id.startswith("AC"):
            errors.append("contact_id must start with 'AC'")
        if self.contact_type == ContactType.physical and not self.is_verified:
            errors.append("Physical contacts must be verified")
        if self.witness_count < 3:
            errors.append("not enough witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            errors.append("message required for high signals")

        if errors:
            raise ValueError(errors)

        return self


def main() -> None:
    print("\nAlien Contact Log Validation")
    print("=" * 30)
    print()

    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.now(),
        contact_type=ContactType.physical,
        location="Area 51, Nevada",
        signal_strength=0.85,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True,
    )

    print("Valid contact report:")
    print("ID:", contact.contact_id)
    print("Type:", contact.contact_type)
    print("Location:", contact.location)
    print("Signal:", contact.signal_strength)
    print("Duration:", contact.duration_minutes)
    print("Witness:", contact.witness_count)
    print("Message:", contact.message_received)

    print()
    print("=" * 30)

    try:
        AlienContact(
            contact_id="CC_2024_001",
            timestamp=datetime.now(),
            contact_type=ContactType.physical,
            location="Area 51, Nevada",
            signal_strength=0.85,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
        )
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
