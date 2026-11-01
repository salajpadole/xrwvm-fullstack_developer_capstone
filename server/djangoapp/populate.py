import json
from pathlib import Path

from .models import Dealer


def initiate():
    """
    Load the 50 dealership records supplied with the capstone project.
    Safe to run more than once: existing records are updated by ID.
    """
    data_file = (
        Path(__file__).resolve().parent.parent
        / "database"
        / "data"
        / "dealerships.json"
    )

    if not data_file.exists():
        # The repository stores the source JSON beside the database package.
        data_file = (
            Path(__file__).resolve().parents[1]
            / "database"
            / "data"
            / "dealerships.json"
        )

    with data_file.open(encoding="utf-8") as file:
        records = json.load(file).get("dealerships", [])

    if not records:
        raise ValueError(f"No dealership records found in {data_file}")

    for item in records:
        Dealer.objects.update_or_create(
            id=item["id"],
            defaults={
                "full_name": item["full_name"],
                "city": item["city"],
                "state": item["state"],
                "address": item["address"],
                "zip": item["zip"],
                "lat": str(item["lat"]),
                "long": str(item["long"]),
                "short_name": item["short_name"],
            },
        )

    print(f"Successfully loaded {len(records)} dealerships.")
