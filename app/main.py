from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.temperature import (
    AbsoluteZeroError,
    TemperatureUnit,
    celsius_to_fahrenheit,
    convert_temperature,
    fahrenheit_to_celsius,
)
from app.schemas import (
    ConversionResponse,
    ErrorResponse,
    FahrenheitToCelsiusResponse,
    GenericConversionResponse,
    BatchConversionRequest,
    BatchConversionResponse,
    BatchConversionResult,
)

app = FastAPI(
    title="API de conversión de temperatura",
    version="1.0.0",
    description="Convierte temperaturas de grados Celsius a Fahrenheit.",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    del request
    del exc
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "codigo": "VALOR_INVALIDO",
                "mensaje": "El valor debe ser un número válido",
            }
        },
    )


@app.exception_handler(AbsoluteZeroError)
async def absolute_zero_exception_handler(
    request: Request, exc: AbsoluteZeroError
) -> JSONResponse:
    del request
    del exc
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "codigo": "BAJO_CERO_ABSOLUTO",
                "mensaje": (
                    f"El valor no puede ser inferior a "
                    f"{exc.minimum} º{exc.unit.value}"
                ),
            }
        },
    )


@app.get(
    "/api/v1/celsius-a-fahrenheit",
    response_model=ConversionResponse,
    responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
    deprecated=True,
)
async def convertir_celsius_a_fahrenheit(
    valor: float = Query(..., description="Temperatura en grados Celsius.")
) -> ConversionResponse:
    return ConversionResponse(
        celsius=valor,
        fahrenheit=celsius_to_fahrenheit(valor),
    )


@app.get(
    "/api/v1/fahrenheit-a-celsius",
    response_model=FahrenheitToCelsiusResponse,
    responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
    deprecated=True,
)
async def convertir_fahrenheit_a_celsius(
    valor: float = Query(..., description="Temperatura en grados Fahrenheit.")
) -> FahrenheitToCelsiusResponse:
    return FahrenheitToCelsiusResponse(
        fahrenheit=valor,
        celsius=fahrenheit_to_celsius(valor),
    )


@app.get(
    "/api/v2/conversion",
    response_model=GenericConversionResponse,
    responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
async def convertir(
    valor: float = Query(..., description="Valor de la temperatura."),
    desde: TemperatureUnit = Query(..., description="Unidad de origen: C, F o K."),
    hasta: TemperatureUnit = Query(
        ..., description="Unidad de destino: C, F o K."
    ),
) -> GenericConversionResponse:
    return GenericConversionResponse(
        valor=valor,
        desde=desde.value,
        hasta=hasta.value,
        resultado=convert_temperature(valor, desde, hasta),
    )


@app.post(
    "/api/v2/conversiones",
    response_model=BatchConversionResponse,
    response_model_exclude_none=True,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
    },
)
async def convertir_lote(
    request: BatchConversionRequest,
) -> BatchConversionResponse | JSONResponse:
    if len(request.conversiones) > 100:
        return JSONResponse(
            status_code=413,
            content={
                "error": {
                    "codigo": "LIMITE_ELEMENTOS_EXCEDIDO",
                    "mensaje": "La petición no puede contener más de 100 conversiones",
                }
            },
        )

    resultados: list[BatchConversionResult] = []
    for conversion in request.conversiones:
        try:
            resultado = convert_temperature(
                conversion.valor, conversion.desde, conversion.hasta
            )
            resultados.append(
                BatchConversionResult(
                    valor=conversion.valor,
                    desde=conversion.desde,
                    hasta=conversion.hasta,
                    resultado=resultado,
                )
            )
        except AbsoluteZeroError as exc:
            resultados.append(
                BatchConversionResult(
                    valor=conversion.valor,
                    desde=conversion.desde,
                    hasta=conversion.hasta,
                    error={
                        "codigo": "BAJO_CERO_ABSOLUTO",
                        "mensaje": (
                            f"El valor no puede ser inferior a "
                            f"{exc.minimum} º{exc.unit.value}"
                        ),
                    },
                )
            )

    return BatchConversionResponse(resultados=resultados)
