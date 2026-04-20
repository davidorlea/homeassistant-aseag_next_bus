"""Tests for ASEAG Next Bus Sensor."""

from datetime import UTC, datetime, timedelta
import json
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
import pytest
import requests
import requests_mock

from custom_components.aseag_next_bus.sensor import AseagApi, AseagNextBusSensor


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
    api_response: Any, requests_mock: requests_mock.Mocker
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
    assert "delay" not in sensor.extra_state_attributes
    assert "line" not in sensor.extra_state_attributes
    assert "destination" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


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
    api_response: Any, requests_mock: requests_mock.Mocker
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
    assert "predictions" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


def test_sensor_in_single_mode_with_malformed_response(
    requests_mock: requests_mock.Mocker,
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
    assert "delay" not in sensor.extra_state_attributes
    assert "line" not in sensor.extra_state_attributes
    assert "destination" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


def test_sensor_in_list_mode_with_malformed_response(
    requests_mock: requests_mock.Mocker,
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
    assert "predictions" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


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
    assert "delay" not in sensor.extra_state_attributes
    assert "line" not in sensor.extra_state_attributes
    assert "destination" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


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
    assert "predictions" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


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
    assert "delay" not in sensor.extra_state_attributes
    assert "line" not in sensor.extra_state_attributes
    assert "destination" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


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
    assert "predictions" not in sensor.extra_state_attributes
    assert "attribution" not in sensor.extra_state_attributes


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
    assert sensor.extra_state_attributes["delay"] == 0
    assert sensor.extra_state_attributes["line"] == "1"
    assert sensor.extra_state_attributes["destination"] == "One"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert len(sensor.extra_state_attributes["predictions"]) == 2
    assert (
        sensor.extra_state_attributes["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=5)
        ).isoformat()
    )
    assert sensor.extra_state_attributes["predictions"][0]["delay"] == 0
    assert sensor.extra_state_attributes["predictions"][0]["line"] == "1"
    assert sensor.extra_state_attributes["predictions"][0]["destination"] == "One"
    assert (
        sensor.extra_state_attributes["predictions"][1]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert sensor.extra_state_attributes["predictions"][1]["delay"] == 0
    assert sensor.extra_state_attributes["predictions"][1]["line"] == "2"
    assert sensor.extra_state_attributes["predictions"][1]["destination"] == "Two"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert sensor.extra_state_attributes["delay"] is None
    assert sensor.extra_state_attributes["line"] == "1"
    assert sensor.extra_state_attributes["destination"] == "One"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert len(sensor.extra_state_attributes["predictions"]) == 2
    assert (
        sensor.extra_state_attributes["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=5)
        ).isoformat()
    )
    assert sensor.extra_state_attributes["predictions"][0]["delay"] is None
    assert sensor.extra_state_attributes["predictions"][0]["line"] == "1"
    assert sensor.extra_state_attributes["predictions"][0]["destination"] == "One"
    assert (
        sensor.extra_state_attributes["predictions"][1]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert sensor.extra_state_attributes["predictions"][1]["delay"] is None
    assert sensor.extra_state_attributes["predictions"][1]["line"] == "2"
    assert sensor.extra_state_attributes["predictions"][1]["destination"] == "Two"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert sensor.extra_state_attributes["delay"] == 0
    assert sensor.extra_state_attributes["line"] == "2"
    assert sensor.extra_state_attributes["destination"] == "Two"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert len(sensor.extra_state_attributes["predictions"]) == 1
    assert (
        sensor.extra_state_attributes["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert sensor.extra_state_attributes["predictions"][0]["delay"] == 0
    assert sensor.extra_state_attributes["predictions"][0]["line"] == "2"
    assert sensor.extra_state_attributes["predictions"][0]["destination"] == "Two"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert sensor.extra_state_attributes["delay"] == 0
    assert sensor.extra_state_attributes["line"] == "2"
    assert sensor.extra_state_attributes["destination"] == "Two"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"


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
    assert len(sensor.extra_state_attributes["predictions"]) == 1
    assert (
        sensor.extra_state_attributes["predictions"][0]["departure"]
        == (
            datetime.now(tz=UTC).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert sensor.extra_state_attributes["predictions"][0]["delay"] == 0
    assert sensor.extra_state_attributes["predictions"][0]["line"] == "2"
    assert sensor.extra_state_attributes["predictions"][0]["destination"] == "Two"
    assert sensor.extra_state_attributes["attribution"] == "Data provided by ASEAG"
