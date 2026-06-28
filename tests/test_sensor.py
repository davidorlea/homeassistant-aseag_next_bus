"""Tests for ASEAG Next Bus Sensor."""

from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
import json
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
import pytest
import requests
import requests_mock

from custom_components.aseag_next_bus.sensor import AseagApi, AseagNextBusSensor


def extra_state_attributes(sensor: AseagNextBusSensor) -> Mapping[str, Any]:
    """Return sensor attributes with a non-optional type for assertions."""
    assert sensor.extra_state_attributes is not None
    return sensor.extra_state_attributes


@pytest.mark.parametrize(
    "api_response",
    [
        None,
        "",
        {},
        {"departures": None},
        {"departures": {}},
        {"departures": {"departures": None}},
        {"departures": {"departures": []}},
    ],
)
def test_sensor_in_single_mode_with_empty_response(
    api_response: Any, requests_mock: requests_mock.Mocker, caplog: Any
) -> None:
    """Test that sensor in single mode with empty response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=json.dumps(api_response),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.state is None
    assert "delay" not in extra_state_attributes(sensor)
    assert "line" not in extra_state_attributes(sensor)
    assert "destination" not in extra_state_attributes(sensor)
    assert "tracking" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"
    assert "Error parsing data" not in caplog.text
    assert "Erroneous result found" not in caplog.text


@pytest.mark.parametrize(
    "api_response",
    [
        None,
        "",
        {},
        {"departures": None},
        {"departures": {}},
        {"departures": {"departures": None}},
        {"departures": {"departures": []}},
    ],
)
def test_sensor_in_list_mode_with_empty_response(
    api_response: Any, requests_mock: requests_mock.Mocker, caplog: Any
) -> None:
    """Test that sensor in list mode with empty response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=json.dumps(api_response),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state is None
    assert "predictions" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"
    assert "Error parsing data" not in caplog.text
    assert "Erroneous result found" not in caplog.text


def test_sensor_in_single_mode_with_malformed_response(
    requests_mock: requests_mock.Mocker, caplog: Any
) -> None:
    """Test that sensor in single mode with malformed response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text="some text",
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.state is None
    assert "delay" not in extra_state_attributes(sensor)
    assert "line" not in extra_state_attributes(sensor)
    assert "destination" not in extra_state_attributes(sensor)
    assert "tracking" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"
    assert "Error parsing data" in caplog.text
    assert "Erroneous result found" not in caplog.text


def test_sensor_in_list_mode_with_malformed_response(
    requests_mock: requests_mock.Mocker, caplog: Any
) -> None:
    """Test that sensor in list mode with malformed response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text="some text",
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state is None
    assert "predictions" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"
    assert "Error parsing data" in caplog.text
    assert "Erroneous result found" not in caplog.text


@pytest.mark.parametrize(
    "api_response",
    [
        {"departures": "some text"},
        {"departures": {"departures": [{}]}},
        {"departures": {"departures": 123}},
    ],
)
def test_sensor_in_single_mode_with_malformed_departures(
    api_response: Any, requests_mock: requests_mock.Mocker, caplog: Any
) -> None:
    """Test that sensor in single mode handles malformed departures."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=json.dumps(api_response),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.state is None
    assert "delay" not in extra_state_attributes(sensor)
    assert "line" not in extra_state_attributes(sensor)
    assert "destination" not in extra_state_attributes(sensor)
    assert "tracking" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"
    assert "Error parsing data" not in caplog.text
    assert "Erroneous result found" in caplog.text


@pytest.mark.parametrize(
    "api_response",
    [
        {"departures": "some text"},
        {"departures": {"departures": [{}]}},
        {"departures": {"departures": 123}},
    ],
)
def test_sensor_in_list_mode_with_malformed_departures(
    api_response: Any, requests_mock: requests_mock.Mocker, caplog: Any
) -> None:
    """Test that sensor in list mode handles malformed departures."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=json.dumps(api_response),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state is None
    assert "predictions" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"
    assert "Error parsing data" not in caplog.text
    assert "Erroneous result found" in caplog.text


def test_sensor_in_single_mode_with_error_response(
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with error response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        status_code=500,
        text="some error",
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.state is None
    assert "delay" not in extra_state_attributes(sensor)
    assert "line" not in extra_state_attributes(sensor)
    assert "destination" not in extra_state_attributes(sensor)
    assert "tracking" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_error_response(
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with error response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        status_code=500,
        text="some error",
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state is None
    assert "predictions" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_no_response(
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with no response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        exc=requests.exceptions.ConnectionError,
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.state is None
    assert "delay" not in extra_state_attributes(sensor)
    assert "line" not in extra_state_attributes(sensor)
    assert "destination" not in extra_state_attributes(sensor)
    assert "tracking" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_no_response(
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with no response returns correct properties."""
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        exc=requests.exceptions.ConnectionError,
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state is None
    assert "predictions" not in extra_state_attributes(sensor)
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(3)
        .with_actual_time_delta(3)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=3)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode returns correct properties."""
    prediction_one = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(5)
        .with_actual_time_delta(5)
        .build()
    )
    prediction_two = (
        create_prediction()
        .with_line_name("2")
        .with_destination_text("Two")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction_one, prediction_two]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 2
    assert len(extra_state_attributes(sensor)["predictions"]) == 2
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=5)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert (
        extra_state_attributes(sensor)["predictions"][1]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][1]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][1]["line"] == "2"
    assert extra_state_attributes(sensor)["predictions"][1]["destination"] == "Two"
    assert extra_state_attributes(sensor)["predictions"][1]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_missing_actual_time(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with missing actual time returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(3)
        .without_actual_time()
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=3)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_missing_actual_time(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with missing actual time returns correct properties."""
    prediction_one = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(5)
        .without_actual_time()
        .build()
    )
    prediction_two = (
        create_prediction()
        .with_line_name("2")
        .with_destination_text("Two")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction_one, prediction_two]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 2
    assert len(extra_state_attributes(sensor)["predictions"]) == 2
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=5)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert (
        extra_state_attributes(sensor)["predictions"][1]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][1]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][1]["line"] == "2"
    assert extra_state_attributes(sensor)["predictions"][1]["destination"] == "Two"
    assert extra_state_attributes(sensor)["predictions"][1]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_cancellation(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with cancellation returns correct properties."""
    prediction_one = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(5)
        .with_actual_time_delta(5)
        .with_cancelled(True)
        .build()
    )
    prediction_two = (
        create_prediction()
        .with_line_name("2")
        .with_destination_text("Two")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction_one, prediction_two]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "2"
    assert extra_state_attributes(sensor)["destination"] == "Two"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_cancellation(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with cancellation returns correct properties."""
    prediction_one = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(5)
        .with_actual_time_delta(5)
        .with_cancelled(True)
        .build()
    )
    prediction_two = (
        create_prediction()
        .with_line_name("2")
        .with_destination_text("Two")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction_one, prediction_two]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "2"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "Two"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_scheduled_to_cached(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from scheduled to cached returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_scheduled_to_cached(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from scheduled to cached returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_live_to_cached(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from live to cached returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_live_to_cached(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from live to cached returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_live_to_live(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from live to live returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([prediction])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_live_to_live(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from live to live returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([prediction])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_live_to_scheduled(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from live to scheduled returns correct properties."""
    prediction_live = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    prediction_scheduled = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    prediction_scheduled["stopPrediction"]["tripId"] = prediction_live[
        "stopPrediction"
    ]["tripId"]
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction_live])},
            {"text": create_api_response([prediction_scheduled])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_live_to_scheduled(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from live to scheduled returns correct properties."""
    prediction_live = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    prediction_scheduled = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    prediction_scheduled["stopPrediction"]["tripId"] = prediction_live[
        "stopPrediction"
    ]["tripId"]
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction_live])},
            {"text": create_api_response([prediction_scheduled])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_scheduled_to_live(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from scheduled to live returns correct properties."""
    prediction_scheduled = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    prediction_live = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    prediction_live["stopPrediction"]["tripId"] = prediction_scheduled[
        "stopPrediction"
    ]["tripId"]
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction_scheduled])},
            {"text": create_api_response([prediction_live])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_scheduled_to_live(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from scheduled to live returns correct properties."""
    prediction_scheduled = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    prediction_live = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    prediction_live["stopPrediction"]["tripId"] = prediction_scheduled[
        "stopPrediction"
    ]["tripId"]
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction_scheduled])},
            {"text": create_api_response([prediction_live])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_scheduled_to_scheduled(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from scheduled to scheduled returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([prediction])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_scheduled_to_scheduled(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from scheduled to scheduled returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([prediction])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_cached_to_cached(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from cached to cached returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
            {"text": create_api_response([])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_cached_to_cached(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from cached to cached returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
            {"text": create_api_response([])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_cached_to_live(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from cached to live returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
            {"text": create_api_response([prediction])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_cached_to_live(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from cached to live returns correct properties."""
    prediction = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction])},
            {"text": create_api_response([])},
            {"text": create_api_response([prediction])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_tracking_cached_to_scheduled(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with tracking from cached to scheduled returns correct properties."""
    prediction_live = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    prediction_scheduled = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    prediction_scheduled["stopPrediction"]["tripId"] = prediction_live[
        "stopPrediction"
    ]["tripId"]
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction_live])},
            {"text": create_api_response([])},
            {"text": create_api_response([prediction_scheduled])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] is None
    assert extra_state_attributes(sensor)["line"] == "1"
    assert extra_state_attributes(sensor)["destination"] == "One"
    assert extra_state_attributes(sensor)["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_tracking_cached_to_scheduled(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with tracking from cached to scheduled returns correct properties."""
    prediction_live = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    prediction_scheduled = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(10)
        .without_actual_time()
        .build()
    )
    prediction_scheduled["stopPrediction"]["tripId"] = prediction_live[
        "stopPrediction"
    ]["tripId"]
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        [
            {"text": create_api_response([prediction_live])},
            {"text": create_api_response([])},
            {"text": create_api_response([prediction_scheduled])},
        ],
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "cached"
    assert sensor.attribution == "Data provided by ASEAG"

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] is None
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "1"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "One"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "scheduled"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_single_mode_with_stop_cancellation(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in single mode with stop cancellation returns correct properties."""
    prediction_one = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(5)
        .with_actual_time_delta(5)
        .with_stop_cancelled(True)
        .build()
    )
    prediction_two = (
        create_prediction()
        .with_line_name("2")
        .with_destination_text("Two")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction_one, prediction_two]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "single", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert (
        sensor.state
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["delay"] == 0
    assert extra_state_attributes(sensor)["line"] == "2"
    assert extra_state_attributes(sensor)["destination"] == "Two"
    assert extra_state_attributes(sensor)["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"


def test_sensor_in_list_mode_with_stop_cancellation(
    create_prediction: Any,
    create_api_response: Any,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test that sensor in list mode with stop cancellation returns correct properties."""
    prediction_one = (
        create_prediction()
        .with_line_name("1")
        .with_destination_text("One")
        .with_planned_time_delta(5)
        .with_actual_time_delta(5)
        .with_stop_cancelled(True)
        .build()
    )
    prediction_two = (
        create_prediction()
        .with_line_name("2")
        .with_destination_text("Two")
        .with_planned_time_delta(10)
        .with_actual_time_delta(10)
        .build()
    )
    requests_mock.get(
        "https://mova.aseag.de/mbroker/rest/areainformation/12345",
        text=create_api_response([prediction_one, prediction_two]),
    )
    sensor = AseagNextBusSensor(AseagApi(), "Sensor", "list", "12345", "H.1")

    sensor.update()

    assert sensor.name == "Sensor 12345 H.1"
    assert sensor.icon == "mdi:bus"
    assert sensor.device_class is None
    assert sensor.state == 1
    assert len(extra_state_attributes(sensor)["predictions"]) == 1
    assert (
        extra_state_attributes(sensor)["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert extra_state_attributes(sensor)["predictions"][0]["delay"] == 0
    assert extra_state_attributes(sensor)["predictions"][0]["line"] == "2"
    assert extra_state_attributes(sensor)["predictions"][0]["destination"] == "Two"
    assert extra_state_attributes(sensor)["predictions"][0]["tracking"] == "live"
    assert sensor.attribution == "Data provided by ASEAG"
