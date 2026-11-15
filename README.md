# Proyecto ING200 — Optimización 2026-2

## Fiesta de Verano de Villa Peumayén

Modelo de programación lineal entera para decidir qué tres artistas se presentan cada noche del
festival, en qué recinto, maximizando el público total esperado bajo restricciones de presupuesto,
disponibilidad, exclusividad y plan de seguridad.

**Curso:** ING200 — Optimización, Universidad Adolfo Ibáñez
**Integrantes:** _(completar)_

---

## Contenido del repositorio

| Archivo | Descripción |
| :--- | :--- |
| `proyecto.ipynb` | Notebook completo con (a), (b), (c) y (d). Pensado para Google Colab + `gurobipy`. |
| `informe_proyecto.md` | Informe de respaldo con formulación, resultados, tablas y análisis. |
| `datos_festival.py` | Datos del problema y función de demanda entregados por el curso. |
| `proyecto_optimizaci_n_2026_2.md` | Enunciado del proyecto. |
| `figuras/` | Gráficos usados en el informe. |

---

## Solución base (b)

| Noche | Recinto | Artistas | Público |
| :--- | :--- | :--- | ---: |
| Viernes | Plaza de Armas | Kevo Flow, Los Cumbiancheros del Ñuble, Las Hermanas Quintral | 9.657 |
| Sábado | Medialuna | Camila Arrebol, Grupo Tierra Sur, Niebla Austral | 7.045 |
| Domingo | Gimnasio Municipal | Ruta Cinco, Banda Fogata, Tomás del Lago | 3.297 |
| **Total** | | | **19.999** |

- **Costo total:** 249 MM$ (193 artistas + 56 recintos).
- **Plan de seguridad:** no se requiere (el público no supera las 20.000 personas).

---

## Enfoque de modelamiento

El público de un trío de artistas **no es aditivo** (hay interacción por pares y efecto arrastre de
los artistas grandes), pero como cada noche tiene exactamente tres artistas el conjunto de programas
posibles es finito. El modelo **precalcula** el público y el costo de cada combinación
(trío, noche, recinto) y luego resuelve un modelo de partición de conjuntos con variables binarias:

- $X_{cnr} \in \{0,1\}$: el trío $c$ toca la noche $n$ en el recinto $r$.
- $Y \in \{0,1\}$: se implementa el plan de seguridad.

Esto mantiene el modelo **lineal entero puro** y exacto: 377 tríos válidos, 3.156 variables, 21
restricciones. Se resuelve en dos etapas (primero maximizar público, luego minimizar costo con el
óptimo fijado) para implementar el desempate pedido en la pauta.

---

## Resultados principales

| Pregunta | Resultado |
| :--- | :--- |
| (b) Público total | 19.999 personas |
| (b) Costo total | 249 MM$ |
| (b) Plan de seguridad | No se requiere |
| (c) I Noche más frágil | Sábado: sin Camila Arrebol cae 71,8 % (1.986) |
| (c) III Condición recomendada | A4: a lo más 1 artista pequeño por noche (−1 persona, peor caso 1.544 → 2.599) |
| (d) II Noche más desmejorada | Domingo |
| (d) IV Nivel recomendado | Piso de 6.000 personas por noche (−12 personas, domingo 3.297 → 6.219) |

El detalle completo, con las tablas de cada escenario y la justificación, está en
[`informe_proyecto.md`](informe_proyecto.md).

---

## Cómo ejecutar

1. Abrir `proyecto.ipynb` en Google Colab.
2. Ejecutar la primera celda: instala `gurobipy` y monta la licencia desde Google Drive.
   Si la licencia está en otra ruta, ajustar `GRB_LICENSE_FILE`.
3. Ejecutar el resto de las celdas en orden.

El notebook fija `MIPGap = 0` y `MIPGapAbs = 0` para garantizar optimalidad exacta, tal como exige
el enunciado. La búsqueda del presupuesto mínimo de (d) IV usa bisección (el público máximo es no
decreciente en el presupuesto), por lo que obtiene el valor exacto con pocas resoluciones por nivel.
