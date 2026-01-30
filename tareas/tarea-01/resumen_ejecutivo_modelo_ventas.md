# Optimizar el inventario exige transformar la forma en que se pronostica la demanda.

---

## Implementar pronósticos con Machine Learning es la palanca clave para recuperar margen y disponibilidad.

La compañía enfrenta pérdidas relevantes de margen, ventas y lealtad del cliente debido a una baja precisión en el pronóstico de demanda.  
Recomendamos implementar un modelo de Machine Learning como motor principal de planificación, dado que reduce el error de pronóstico en **35–40%** y habilita decisiones más rápidas y confiables.

**Objetivos estratégicos impactados directamente**
- Margen operativo: **8.5%**
- Inventory turnover: **6.2x → 9x anual**

---

## El desbalance de inventario ya está generando pérdidas financieras y comerciales

- **23% del inventario en sobrestock**
  - Costos elevados de almacenamiento
  - Liquidaciones con descuentos promedio de **~35%**
- **Quiebres de stock en 18% del tiempo** en productos clave
  - Ventas perdidas estimadas en **USD 6.8M anuales**
- **–12 puntos en NPS** por faltantes recurrentes

📌 El negocio pierde valor tanto por exceso como por escasez de inventario.

---

## El análisis exploratorio confirma una alta volatilidad y heterogeneidad de la demanda

> *Los patrones de demanda varían significativamente por producto, tienda y estacionalidad, superando la capacidad del enfoque actual.*

<!-- INSERTAR IMAGEN EDA 1 -->

![Distribución de la demanda por producto-tienda-](reports/Eda_demand_distribution.png)


<!-- INSERTAR IMAGEN EDA 2 -->
<!-- Ejemplo: Estacionalidad / patrones temporales -->

![Patrones de estacionalidad en ventas](reports/Eda_demand_distribution.png)

---

## El modelo actual de planeación no escala a la complejidad del negocio

- **22,000+ productos en 60 tiendas**
- Pronósticos basados en:
  - Promedios móviles
  - Ajustes manuales
- Decisiones con **14 días de anticipación**
  - La competencia ajusta en **48 horas**
- Resultado:
  - **RMSE ≈ 11 unidades**
  - Margen operativo por debajo de lo esperado

---

## La baja precisión del pronóstico está destruyendo valor financiero y comercial

**¿Cómo puede la compañía anticipar mejor la demanda para reducir sobrestock y quiebres, sin incrementar la carga operativa del equipo?**

---

## El modelo de Machine Learning anticipa la demanda con mayor granularidad y oportunidad

El equipo de Ciencia de Datos desarrolló un modelo que:

- Usa **3 años de datos transaccionales**  
  (>2.9M registros diarios)
- Predice ventas a nivel **producto–tienda–mes**
- Captura:
  - Tendencias
  - Estacionalidad
  - Variabilidad local
- Genera **intervalos de confianza** para gestión de riesgo
- Es **automatizable y escalable**, con actualización diaria

---

## El modelo reduce significativamente el error frente al enfoque tradicional

### La precisión mejora de forma consistente
- **RMSE**
  - Baseline: ~11  
  - ML: ~7  
  - **–35% de error**
- **MAE**
  - Baseline: ~8  
  - ML: ~5  
  - **–40% de error**

<!-- INSERTAR IMAGEN EDA / MODEL 3 -->
<!-- Ejemplo: Comparación RMSE baseline vs ML -->

![Comparación de RMSE: Baseline vs ML](docs/images/rmse_comparison.png)

---

## La reducción del error se traduce en mayor estabilidad operativa

- Menor variabilidad en errores de predicción
- Menos casos extremos de sobrestock o quiebres
- Mayor confiabilidad para decisiones de reabastecimiento

<!-- INSERTAR IMAGEN EDA / MODEL 4 -->
<!-- Ejemplo: Distribución de errores -->

![Distribución de errores de predicción](docs/images/error_distribution.png)

---

## Integrar el modelo en la operación permite capturar valor rápidamente

**Recomendación de implementación**
- Integrar predicciones al sistema de gestión de inventarios
- Ajustar automáticamente sugerencias de reabastecimiento
- Configurar alertas ante predicciones atípicas

**Estrategia de adopción**
- Piloto en categorías con demanda estable
- Uso paralelo al método actual
- Escalamiento progresivo

---

## La automatización libera al equipo para decisiones estratégicas

- Hasta **70% de los pronósticos rutinarios** automatizados
- Menor carga manual
- Planificadores enfocados en excepciones y escenarios especiales

---

## El modelo debe guiar decisiones, no reemplazar el criterio en escenarios inciertos

- Alta confiabilidad en:
  - Demanda estable
  - Estacionalidad regular
  - Productos con historial suficiente
- En lanzamientos o campañas:
  - Usar el modelo con precaución
  - Complementarlo con expertise del negocio

---

## Mejorar el pronóstico es la forma más directa de corregir el inventario

El problema central no es el inventario, sino la **precisión en la predicción de la demanda**.  
El modelo de Machine Learning demuestra que puede cerrar esta brecha y habilitar una operación más rentable, ágil y centrada en el cliente.