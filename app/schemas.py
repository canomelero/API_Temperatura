from pydantic import BaseModel

from app.domain.temperature import TemperatureUnit


class ConversionResponse(BaseModel):
    celsius: float
    fahrenheit: float


class FahrenheitToCelsiusResponse(BaseModel):
    fahrenheit: float
    celsius: float


class GenericConversionResponse(BaseModel):
    valor: float
    desde: str
    hasta: str
    resultado: float


class ConversionRequest(BaseModel):
    valor: float
    desde: TemperatureUnit
    hasta: TemperatureUnit


class BatchConversionRequest(BaseModel):
    conversiones: list[ConversionRequest]


class ErrorDetail(BaseModel):
    codigo: str
    mensaje: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


class BatchConversionResult(BaseModel):
    valor: float
    desde: TemperatureUnit
    hasta: TemperatureUnit
    resultado: float | None = None
    error: ErrorDetail | None = None


class BatchConversionResponse(BaseModel):
    resultados: list[BatchConversionResult]
