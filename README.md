# API de conversión de temperatura

## Contrato

El contrato aprobado de la API está en [`openapi.yaml`](./openapi.yaml).

## Ejecución

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

La documentación interactiva queda disponible en `http://127.0.0.1:8000/docs`.

## Versiones de la API

La versión v2 es la interfaz recomendada para nuevas integraciones:

```text
GET /api/v2/conversion?valor=25&desde=C&hasta=K
```

Devuelve `25 ºC = 298.15 K` y admite las unidades `C`, `F` y `K`.

Para convertir varias temperaturas se utiliza:

```text
POST /api/v2/conversiones
```

El cuerpo debe contener una lista `conversiones` de como máximo 100 elementos.
El lote siempre se procesa completo: los errores de temperatura se devuelven
en el elemento correspondiente y no impiden procesar los demás. Un cuerpo mal
formado devuelve `400` y superar el límite devuelve `413`.

Los endpoints v1 se mantienen temporalmente para compatibilidad con clientes
existentes, pero están marcados como obsoletos. No se añadirán nuevas unidades
ni funcionalidades a v1. Cuando todos los clientes hayan migrado a v2, v1
podrá retirarse en una versión posterior.
