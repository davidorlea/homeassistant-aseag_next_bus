"""Test fixtures for ASEAG Next Bus Sensor."""

from base64 import b64encode
from datetime import datetime, timedelta
import json
from random import randint
from typing import Self

from pytest import fixture


class AseagPredictionFixture:
    """Representation of a ASEAG API prediction fixture."""

    def __init__(self):
        """Initialize the ASEAG API prediction fixture."""
        self._line_name = "Some Line Name"
        self._destination_text = "Some Destination Text"
        self._trip_id = self.__generate_random_trip_id()
        self._planned_time = self.__get_time_from_delta(10)
        self._actual_time = self.__get_time_from_delta(10)
        self._track = "H.1"

    def with_line_name(self, line_name: str) -> Self:
        """Set an individual line name."""
        self._line_name = line_name
        return self

    def with_destination_text(self, destination_text: str) -> Self:
        """Set an individual destination text."""
        self._destination_text = destination_text
        return self

    def with_planned_time_delta(self, minutes: int) -> Self:
        """Set an individual planned time."""
        self._planned_time = self.__get_time_from_delta(minutes)
        return self

    def with_actual_time_delta(self, minutes: int) -> Self:
        """Set an individual actual time."""
        self._actual_time = self.__get_time_from_delta(minutes)
        return self

    def with_track(self, track: str) -> Self:
        """Set an individual track."""
        self._track = track
        return self

    def build(self) -> dict:
        """Return the prediction."""
        return {
            "stopPrediction": {
                "lineName": self._line_name,
                "destinationText": self._destination_text,
                "tripId": self._trip_id,
                "plannedTime": self._planned_time,
                "actualTime": self._actual_time,
                "track": self._track,
            }
        }

    @staticmethod
    def __generate_random_trip_id() -> str:
        """Return a random trip id."""
        trip_id = f"1|{randint(100000, 999999)}|0|{randint(10, 99)}|{randint(10000000, 99999999)}"
        return b64encode(trip_id.encode("utf-8")).decode("utf-8")

    @staticmethod
    def __get_time_from_delta(minutes) -> int:
        """Return a timestamp with given delta from now."""
        return int(
            (
                datetime.now().replace(microsecond=0) + timedelta(minutes=minutes)
            ).timestamp()
            * 1000
        )


class AseagDeparturesFixture:
    """Representation of a ASEAG API fixture."""

    def __init__(self):
        """Initialize the ASEAG API fixture."""
        self._departures = []

    def with_departures(self, predictions: [dict]) -> Self:
        """Set a list of predictions."""
        self._departures = predictions
        return self

    def build(self) -> dict:
        """Return the departures."""
        return {"departures": {"departures": self._departures}}


@fixture()
def create_timestamp_from_delta():
    """Fixture to create a timestamp from a delta."""

    def _create_timestamp_from_delta(now: datetime, minutes: int):
        return int(
            (now.replace(microsecond=0) + timedelta(minutes=minutes)).timestamp() * 1000
        )

    return _create_timestamp_from_delta


@fixture()
def create_prediction():
    """Fixture to create a ASEAG API prediction."""

    def _create_prediction():
        return AseagPredictionFixture()

    return _create_prediction


@fixture()
def create_api_response():
    """Fixture to create a ASEAG API response."""

    def _create_api_response(predictions: [dict]):
        departures = AseagDeparturesFixture().with_departures(predictions).build()
        return json.dumps(departures)

    return _create_api_response
