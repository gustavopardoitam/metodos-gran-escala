# Optimizar el inventario exige transformar la forma en que se pronostica la demanda  
**Marco de referencia: SQCA + MECE (estilo McKinsey)**

---

## Implementar pronósticos con Machine Learning es la palanca clave para recuperar margen y disponibilidad

Se recomienda implementar un modelo de pronóstico de demanda basado en Machine Learning como motor principal del proceso de planificación de inventarios.  
El modelo reduce el error de pronóstico en aproximadamente **35–40%**, mejora la velocidad y precisión de las decisiones operativas y ataca directamente las causas estructurales del sobrestock, los quiebres de stock y la erosión de margen.

Esta iniciativa es crítica para alcanzar los objetivos estratégicos del negocio:
- **Margen operativo objetivo:** 8.5%  
- **Inventory turnover objetivo:** 9x anual  

---

## La complejidad operativa del negocio supera la capacidad del enfoque actual de planeación

- La compañía gestiona **más de 22,000 productos en 60 tiendas**, con patrones de demanda altamente heterogéneos.
- El proceso actual de planeación se apoya en:
  - Promedios móviles
  - Ajustes manuales por parte de los planificadores
- Las decisiones de inventario se toman con **14 días de anticipación**, frente a competidores que reaccionan en **48 horas**.
- El negocio dispone de **3 años de datos históricos**, equivalentes a **2.9 millones de registros de ventas diarias**, que hoy no se explotan plenamente.

---

## La baja precisión del pronóstico está destruyendo valor financiero y comercial

### El inventario desbalanceado genera costos evitables
- **23% del inventario se encuentra en sobrestock**
  - Costos elevados de almacenamiento
  - Liquidaciones con descuentos promedio de **~35%**

### Los quiebres de stock están erosionando ingresos y confianza del cliente
- **Quiebres en 18% del tiempo** en productos clave
  - Ventas perdidas estimadas en **USD 6.8 millones anuales**

### La experiencia del cliente se deteriora de forma tangible
- **Caída de 12 puntos en el Net Promoter Score (NPS)**
- Menor lealtad y repetición de compra

### El origen del problema es un pronóstico estructuralmente impreciso
- Error elevado en la predicción de ventas (**RMSE ≈ 11 unidades**)
- El método actual no captura:
  - Variabilidad producto–tienda
  - Estacionalidad
  - Escala y complejidad del portafolio

---

## La pregunta crítica no es de inventario, sino de predicción

**¿Cómo puede la compañía mejorar de forma sustancial la precisión del pronóstico de demanda para reducir sobrestock y quiebres, recuperar margen y acelerar la toma de decisiones operativas?**

---

## Un modelo de Machine Learning permite anticipar la demanda con granularidad y escala

El equipo de Ciencia de Datos desarrolló un modelo de pronóstico que:

- Explota los **3 años de datos históricos transaccionales**
- Genera predicciones a nivel **producto–tienda–mes**
- Identifica patrones complejos de tendencia y estacionalidad
- Produce **intervalos de confianza** para cuantificar incertidumbre
- Es **escalable y automatizable**, con capacidad de actualización diaria

Este enfoque reemplaza un proceso reactivo por uno **predictivo y proactivo**.

---

## El modelo demuestra mejoras cuantificables frente al enfoque tradicional

La evaluación compara el modelo de Machine Learning contra un enfoque baseline (pronóstico naive).

### El error de pronóstico se reduce de forma significativa
- **RMSE**
  - Baseline: ~11 unidades  
  - Modelo ML: ~7 unidades  
  - **Reducción de error: ~35%**

- **MAE**
  - Baseline: ~8 unidades  
  - Modelo ML: ~5 unidades  
  - **Reducción de error: ~40%**

### La consistencia del pronóstico mejora, no solo el promedio
- Menor dispersión de errores
- Menos casos extremos de sobreestimación o subestimación
- Mayor confiabilidad operativa

El desempeño se acerca al objetivo estratégico de **RMSE < 5 unidades por producto–tienda**.

---

## Mejorar el pronóstico impacta directamente las principales palancas del negocio

### Inventario: menos exceso, mayor rotación
- Reducción del sobrestock
- Menor necesidad de liquidaciones
- Avance hacia el objetivo de **9x de rotación**

### Ventas: mayor disponibilidad en góndola
- Disminución de quiebres en productos clave
- Recuperación de ventas perdidas
- Mejor ejecución en temporadas críticas

### Costos y productividad: automatizar para escalar
- Automatización de hasta **70% de los pronósticos rutinarios**
- Reducción significativa del trabajo manual
- Planificadores enfocados en excepciones y decisiones estratégicas

### Cliente: restaurar la confianza en la disponibilidad
- Menos faltantes percibidos
- Recuperación progresiva del NPS

---

## La integración gradual reduce el riesgo y acelera la adopción

### Piloto: probar impacto real en condiciones controladas
- Uso paralelo del modelo ML y el método actual
- Categorías con demanda estable y buen historial
- Medición directa de impacto en inventarios y ventas

### Escalamiento: integrar el modelo al core operativo
- Alimentar el sistema de gestión de inventarios
- Ajuste automático de sugerencias de reabastecimiento
- Alertas ante predicciones atípicas o restricciones operativas

### Automatización: enfocar al equipo en lo que agrega valor
- Uso del modelo como fuente principal de pronóstico
- Automatización del 70% de los casos estándar
- Uso de intervalos de confianza para definir stock de seguridad

---

## El modelo debe guiar decisiones, no reemplazar el criterio en escenarios extremos

El modelo es más confiable cuando:
- Existe historial suficiente
- La demanda es estable o estacional
- Los patrones son consistentes

En escenarios de alta incertidumbre (lanzamientos, promociones atípicas):
- El modelo debe usarse como **input principal**
- Complementarse con criterio experto

---

## Corregir el pronóstico es la forma más directa de corregir el inventario

La compañía no enfrenta un problema aislado de inventario, sino un problema estructural de **precisión en la predicción de la demanda**.  
El modelo de Machine Learning demuestra —con evidencia cuantitativa— que puede cerrar esta brecha de forma escalable, automatizada y alineada con los objetivos estratégicos del negocio.