# Preparación de la habilidad `fridolin-generador-preplanillas`

Estado: 80% preparado. Aún no crear ni instalar la habilidad.

Última verificación: 4 de septiembre de 2026.

## Propósito

Automatizar la lectura del biométrico y del maestro, reconstruir jornadas, aplicar las reglas aprobadas y actualizar en Drive una preplanilla por supervisor. La habilidad termina al entregar documentos de excepciones; no genera todavía la planilla final de Recursos Humanos.

## Entradas obligatorias

- Mes y gestión del ciclo.
- Biométrico RAW completo del periodo.
- `Estructura_PrePlanilla_Fridolin.xlsx`, incluida la pestaña Maestro Empleados.
- Control de vinculación del personal del periodo.
- Tarifas generales y excepciones de jornaleros.
- Identificadores de los documentos de cada supervisor en Drive.

## Secuencia obligatoria

1. Validar encabezados, fechas y marcaciones.
2. Consolidar CI, PIN e ID biométrico bajo una sola persona.
3. Aplicar estado laboral, tipo de personal y supervisor final.
4. Resolver el turno de cada fecha, incluidos cambios dentro del mes.
5. Reconstruir jornadas usando primera entrada y última salida válida.
6. Calcular retrasos, comida, salida temprana y salida tardía.
7. Clasificar impacto informativo o pendiente y calcular consecuencia base.
8. Separar fijos/eventuales, jornaleros, cambios de turno y retirados.
9. Crear o actualizar un documento por supervisor con filtros y fórmulas.
10. Verificar estructura, listas, fórmulas, personas excluidas y tamaño del archivo antes de reemplazarlo en Drive.

## Reglas y formato

La fuente consolidada es `docs/formato-preplanilla-supervisor-v1.md`. La habilidad debe leer y respetar esa versión; no debe duplicar una copia divergente de las reglas.

## Documentos verificados para formar la habilidad

- Medrano: actualizado en Drive, 49 excepciones de fijos/eventuales, 0 jornaleros y 133 registros técnicos.
- Cabrera: actualizado en Drive, 251 excepciones de fijos/eventuales, 8 de jornaleros y 620 registros técnicos.
- Flores: actualizado en Drive, 171 excepciones de fijos/eventuales, 87 de jornaleros y 372 registros técnicos.
- Los tamaños locales coinciden exactamente con los tamaños informados por Drive.
- Los tres libros no presentan errores de fórmula.
- Silvia Chambi no aparece en ninguno de los tres.

## Controles de integridad actuales

- Medrano: 40.979 bytes; SHA-256 `2EEA164B243B3C4B6221798BD8A8D6BB4CD400FF4AF5A212554DF3EE80EEE517`.
- Cabrera: 153.987 bytes; SHA-256 `7BB21DFDF64427A06A9BD0C1984BA51114D40CD21EB8E3F0CCD5F048AA726E70`.
- Flores: 106.179 bytes; SHA-256 `EC9923CD3FF45A1C21988CC91989C59CC03B29B4CC74741B73ADBC05B8C89754`.

## Pendiente para llegar al 100%

- Revisar y aprobar Julia Cruz Olmos.
- Revisar y aprobar Isabel Navarro, incluido el caso Silvia Chambi.
- Confirmar que no existen nuevas correcciones sobre los tres documentos ya actualizados.
- Ejecutar una prueba completa desde entradas originales hasta archivos finales.
- Comparar los resultados de la prueba con los cinco documentos aprobados.
- Crear la habilidad con instrucciones, referencias, scripts reutilizables y controles de seguridad.
- Probar la habilidad en un ciclo controlado antes de usarla en producción.

## Fuera del alcance de esta habilidad

- Interpretar las respuestas finales de los supervisores.
- Consolidar permisos, vacaciones y faltas aprobadas.
- Calcular la bolsa definitiva de horas extra.
- Generar la planilla final para Recursos Humanos.

Estas funciones corresponden a una habilidad posterior denominada provisionalmente `fridolin-cierre-preplanilla`.


