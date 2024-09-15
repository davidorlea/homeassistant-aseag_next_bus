"""Tests for ASEAG Next Bus Sensor."""

from datetime import datetime, timedelta, timezone

import requests_mock

from custom_components.aseag_next_bus.sensor import AseagApi, AseagNextBusSensor
from homeassistant.components.sensor import SensorDeviceClass


def test_sensor_in_single_mode(
    create_prediction, create_api_response, requests_mock: requests_mock.Mocker
):
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
            datetime.now(tz=timezone.utc).replace(microsecond=0) + timedelta(minutes=3)
        ).isoformat()
    )
    assert sensor.extra_state_attributes.get("delay") == 0
    assert sensor.extra_state_attributes.get("line") == "1"
    assert sensor.extra_state_attributes.get("destination") == "One"
    assert sensor.extra_state_attributes.get("attribution") == "Data provided by ASEAG"


def test_sensor_in_multi_mode(
    create_prediction, create_api_response, requests_mock: requests_mock.Mocker
):
    """Test that sensor in multi mode returns correct properties."""
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
    assert len(sensor.extra_state_attributes.get("predictions")) == 2
    assert (
        sensor.extra_state_attributes.get("predictions")[0].get("departure")
        == (
            datetime.now(tz=timezone.utc).replace(microsecond=0) + timedelta(minutes=5)
        ).isoformat()
    )
    assert sensor.extra_state_attributes.get("predictions")[0].get("delay") == 0
    assert sensor.extra_state_attributes.get("predictions")[0].get("line") == "1"
    assert (
        sensor.extra_state_attributes.get("predictions")[0].get("destination") == "One"
    )
    assert (
        sensor.extra_state_attributes.get("predictions")[1].get("departure")
        == (
            datetime.now(tz=timezone.utc).replace(microsecond=0) + timedelta(minutes=10)
        ).isoformat()
    )
    assert sensor.extra_state_attributes.get("predictions")[1].get("delay") == 0
    assert sensor.extra_state_attributes.get("predictions")[1].get("line") == "2"
    assert (
        sensor.extra_state_attributes.get("predictions")[1].get("destination") == "Two"
    )
    assert sensor.extra_state_attributes.get("attribution") == "Data provided by ASEAG"
