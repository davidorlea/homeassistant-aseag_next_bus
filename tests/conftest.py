"""Test fixtures for ASEAG Next Bus Sensor."""

from base64 import b64encode
from collections.abc import Callable
from datetime import datetime, timedelta
import json
from random import randint
from typing import Any, Self

from pytest import fixture


class AseagPredictionFixture:
    """Representation of a ASEAG API prediction fixture."""

    def __init__(self) -> None:
        """Initialize the ASEAG API prediction fixture."""
        self._line_name: str = "Some Line Name"
        self._destination_text: str = "Some Destination Text"
        self._trip_id: str = self.__generate_random_trip_id()
        self._planned_time: int | None = self.__get_time_from_delta(10)
        self._actual_time: int | None = self.__get_time_from_delta(10)
        self._track: str = "H.1"
        self._cancelled: bool = False
        self._stop_cancelled: bool = False

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

    def with_cancelled(self, cancelled: bool) -> Self:
        """Mark the prediction as cancelled."""
        self._cancelled = cancelled
        return self

    def with_stop_cancelled(self, stop_cancelled: bool) -> Self:
        """Mark the stop as cancelled."""
        self._stop_cancelled = stop_cancelled
        return self

    def without_planed_time(self) -> Self:
        """Omit the planned time."""
        self._planned_time = None
        return self

    def without_actual_time(self) -> Self:
        """Omit the actual time."""
        self._actual_time = None
        return self

    def build(self) -> dict[str, Any]:
        """Return the prediction."""
        return {
            "stopPrediction": {
                "lineName": self._line_name,
                "destinationText": self._destination_text,
                "tripId": self._trip_id,
                "plannedTime": self._planned_time,
                "actualTime": self._actual_time,
                "track": self._track,
                "cancelled": self._cancelled,
                "stopCancelled": self._stop_cancelled,
            }
        }

    @staticmethod
    def __generate_random_trip_id() -> str:
        """Return a random trip id."""
        trip_id = f"1|{randint(100000, 999999)}|0|{randint(10, 99)}|{randint(10000000, 99999999)}"
        return b64encode(trip_id.encode("utf-8")).decode("utf-8")

    @staticmethod
    def __get_time_from_delta(minutes: int) -> int:
        """Return a timestamp with given delta from now."""
        return int(
            (
                datetime.now().replace(microsecond=0) + timedelta(minutes=minutes)
            ).timestamp()
            * 1000
        )


class AseagDeparturesFixture:
    """Representation of a ASEAG API fixture."""

    def __init__(self) -> None:
        """Initialize the ASEAG API fixture."""
        self._departures: list[dict[str, Any]] = []

    def with_departures(self, predictions: list[dict[str, Any]]) -> Self:
        """Set a list of predictions."""
        self._departures = predictions
        return self

    def build(self) -> dict[str, Any]:
        """Return the departures."""
        return {"departures": {"departures": self._departures}}


@fixture()
def create_timestamp_from_delta() -> Callable[[datetime, int], int]:
    """Fixture to create a timestamp from a delta."""

    def _create_timestamp_from_delta(now: datetime, minutes: int) -> int:
        return int(
            (now.replace(microsecond=0) + timedelta(minutes=minutes)).timestamp() * 1000
        )

    return _create_timestamp_from_delta


@fixture()
def create_prediction() -> Callable[[], AseagPredictionFixture]:
    """Fixture to create a ASEAG API prediction."""

    def _create_prediction() -> AseagPredictionFixture:
        return AseagPredictionFixture()

    return _create_prediction


@fixture()
def create_api_response() -> Callable[[list[dict[str, Any]]], str]:
    """Fixture to create a ASEAG API response."""

    def _create_api_response(predictions: list[dict[str, Any]]) -> str:
        departures = AseagDeparturesFixture().with_departures(predictions).build()
        return json.dumps(del_none(departures.copy()))

    return _create_api_response


def del_none(d: dict[str, Any]) -> dict[str, Any]:
    """Remove None values from the object."""
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
        elif isinstance(value, list):
            for v in value:
                del_none(v)
    return d
