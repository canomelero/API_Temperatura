from enum import Enum

ABSOLUTE_ZERO_CELSIUS = -273.15


class TemperatureUnit(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


class AbsoluteZeroError(ValueError):
    """Indica que una temperatura está por debajo del cero absoluto."""

    def __init__(self, unit: TemperatureUnit, minimum: float) -> None:
        self.unit = unit
        self.minimum = minimum


def _to_celsius(value: float, unit: TemperatureUnit) -> float:
    if unit is TemperatureUnit.CELSIUS:
        return value
    if unit is TemperatureUnit.FAHRENHEIT:
        return (value - 32) * 5 / 9
    return value - 273.15


def _from_celsius(value: float, unit: TemperatureUnit) -> float:
    if unit is TemperatureUnit.CELSIUS:
        return value
    if unit is TemperatureUnit.FAHRENHEIT:
        return (value * 9 / 5) + 32
    return value + 273.15


def convert_temperature(
    value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit
) -> float:
    """Convierte entre unidades pasando siempre por Celsius."""
    minimums = {
        TemperatureUnit.CELSIUS: -273.15,
        TemperatureUnit.FAHRENHEIT: -459.67,
        TemperatureUnit.KELVIN: 0.0,
    }
    if value < minimums[from_unit]:
        raise AbsoluteZeroError(from_unit, minimums[from_unit])
    return round(_from_celsius(_to_celsius(value, from_unit), to_unit), 2)


def celsius_to_fahrenheit(celsius: float) -> float:
    return convert_temperature(
        celsius, TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT
    )


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return convert_temperature(
        fahrenheit, TemperatureUnit.FAHRENHEIT, TemperatureUnit.CELSIUS
    )
