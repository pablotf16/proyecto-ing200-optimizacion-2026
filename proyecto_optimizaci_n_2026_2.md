# ING200: Optimización — Proyecto
**Universidad Adolfo Ibáñez**  
*Facultad de Ingeniería y Ciencias*

---

## Instrucciones

* El plazo de entrega del proyecto es el día 15 de noviembre a las 23:55 horas.
* Cada minuto después del plazo de entrega tendrá un descuento de 10 puntos de la tarea.
* Se debe entregar un informe de respaldo (en formato digital) en donde se dé respuesta a las preguntas planteadas junto con un archivo de códigos con los que se dieron respuesta a las preguntas.
* La evaluación considera una presentación y defensa oral del trabajo. Cualquier integrante del grupo podrá ser consultado sobre cualquier parte del proyecto.
* Frente a cualquier infracción a deberes de conducta, en especial, la honestidad, será activado un proceso disciplinario al amparo del Código de Honor de la Universidad.

---

## Pregunta 1 [60 puntos]

Cada verano, la Municipalidad de Villa Peumayén organiza su tradicional Fiesta de Verano: tres noches de música (viernes, sábado y domingo) que reúnen a vecinos y visitantes de toda la región. Este año, la municipalidad ha contactado a su grupo como asesores de ingeniería para decidir qué artistas contratar, qué noche se presenta cada uno y en qué recinto se realiza cada noche, de modo de atraer la mayor cantidad de público posible.

### Los artistas

La municipalidad cuenta con 15 artistas candidatos. Cada uno tiene un género musical, un nivel (grande, mediano o pequeño), un índice de popularidad, un costo y las noches en que está disponible:

| Artista | Género | Nivel | Popularidad | Costo ($\text{MM\$}$) | Noches |
| :--- | :--- | :--- | :---: | :---: | :---: |
| La Sonora Copihue | Cumbia | Grande | $1,08$ | $52$ | V, S, D |
| Los Volcanes | Rock | Grande | $0,97$ | $40$ | V, S, D |
| Camila Arrebol | Pop | Grande | $1,03$ | $48$ | V, S, D |
| Kevo Flow | Urbano | Grande | $1,12$ | $58$ | V, S |
| Los Cumbiancheros del Ñuble | Cumbia | Mediano | $0,94$ | $18$ | V, S, D |
| Grupo Tierra Sur | Folclor | Mediano | $1,06$ | $15$ | V, S, D |
| La Nena Real | Urbano | Mediano | $1,01$ | $22$ | V, S, D |
| Las Hermanas Quintral | Pop | Mediano | $0,92$ | $17$ | V, S, D |
| Ruta Cinco | Rock | Mediano | $1,04$ | $16$ | V, S, D |
| Banda Fogata | Cumbia | Pequeño | $1,11$ | $7$ | V, S, D |
| Conjunto Raíces del Valle | Folclor | Pequeño | $0,98$ | $5$ | V, S, D |
| Las Cantoras de Peumayén | Folclor | Pequeño | $0,89$ | $4$ | V, S, D |
| Niebla Austral | Rock | Pequeño | $0,95$ | $6$ | V, S, D |
| Tomás del Lago | Pop | Pequeño | $1,09$ | $8$ | V, S, D |
| Yisus Beat | Urbano | Pequeño | $0,91$ | $6$ | V, S, D |

### Las noches y los recintos

Cada noche se deben considerar exactamente tres artistas, todos en el mismo recinto, con shows de una hora cada uno. La municipalidad puede usar tres recintos, todos disponibles las tres noches:

| Recinto | Capacidad (personas) | Costo de arriendo por noche ($\text{MM\$}$) |
| :--- | :---: | :---: |
| Plaza de Armas | $12.000$ | $30$ |
| Medialuna | $7.500$ | $18$ |
| Gimnasio Municipal | $4.200$ | $8$ |

La asistencia también depende de la noche. Se estima que asiste la siguiente fracción de la demanda de los artistas:

| Noche | Viernes | Sábado | Domingo |
| :--- | :---: | :---: | :---: |
| **Factor de asistencia** $\phi_n$ | $0,90$ | $1,00$ | $0,85$ |

### La demanda esperada

El público que convoca una noche no es simplemente la suma de lo que convoca cada artista por separado: depende de cómo se combinan. La municipalidad cuenta con una función que estima la demanda $D(c)$ de un conjunto de artistas $c$ que se presentan la misma noche:

1. Cada artista $a$ tiene una demanda base:
   $$b_a = (\text{base según su nivel}) \cdot (\text{factor de su género}) \cdot (\text{su popularidad})$$
   con:

   | Nivel | Grande | Mediano | Pequeño |
   | :--- | :---: | :---: | :---: |
   | **Base** | $4.200$ | $1.900$ | $750$ |

   | Género | Cumbia | Pop | Urbano | Rock | Folclor |
   | :--- | :---: | :---: | :---: | :---: | :---: |
   | **Factor** | $1,20$ | $1,00$ | $1,10$ | $0,95$ | $0,65$ |

2. Si en la noche se presenta al menos un artista grande, la demanda base de cada artista mediano o pequeño aumenta un $20\%$ (efecto arrastre).
3. Se calcula un ajuste de interacción $I$ sumando, para cada par de artistas de la noche: $-0,15$ si son del mismo género; $-0,10$ si ambos son grandes; y una afinidad entre géneros de $+0,06$ (cumbia y urbano), $+0,05$ (pop y rock) o $+0,03$ (pop y urbano).
4. La demanda es:
   $$D(c) = \left(\sum_{a \in c} b_a\right)(1 + I)$$

El público esperado de una noche $n$ en el recinto $r$ es $\min\{\phi_n \cdot D(c), K_r\}$, donde $K_r$ es la capacidad del recinto, redondeado al entero más cercano.

> **Ejemplo.** Para La Sonora Copihue, Kevo Flow y Yisus Beat:
> * **Demandas base:** La Sonora Copihue $4.200 \cdot 1,20 \cdot 1,08 = 5.443,2$; Kevo Flow $4.200 \cdot 1,10 \cdot 1,12 = 5.174,4$; Yisus Beat $750 \cdot 1,10 \cdot 0,91 \cdot 1,20 = 900,9$ (con arrastre). Suma: $11.518,5$.
> * **Interacción:** La Sonora Copihue y Kevo Flow ($+0,06 - 0,10$), La Sonora Copihue y Yisus Beat ($+0,06$), Kevo Flow y Yisus Beat ($-0,15$). Total: $I = -0,13$.
> * **Demanda:** $D = 11.518,5 \cdot 0,87 = 10.021,1$. Un viernes en la Plaza de Armas, el público esperado sería $\min\{0,90 \cdot 10.021,1; 12.000\} = 9.019$ personas; en la Medialuna, en cambio, se limitaría a su capacidad de $7.500$.

### Condiciones

1. Cada artista puede presentarse a lo más una vez en el festival, y solo en las noches en que está disponible.
2. Banda Fogata es el telonero de La Sonora Copihue: si se contrata a La Sonora Copihue, Banda Fogata debe presentarse la misma noche.
3. La Nena Real y Yisus Beat mantienen una disputa pública y no aceptan participar en el mismo festival.
4. **Plan de seguridad:** si el público total esperado del festival supera las $20.000$ personas, la municipalidad debe implementar un plan de seguridad, con un costo de $25\text{ MM\$}$.
5. El presupuesto es de $250\text{ MM\$}$ y debe cubrir el costo de los artistas, el arriendo de los recintos y, si corresponde, el plan de seguridad.

El objetivo de la municipalidad es maximizar el público total esperado del festival.

Los datos y la función de demanda se encuentran en el archivo `datos_festival.py`, listo para copiar en su script. El archivo incluye además la función `mostrar_parrilla`, que permite visualizar una solución.

**Importante:** los modelos deben resolverse a optimalidad exacta. En caso de usar Gurobi, fije el parámetro `MIPGap` en $0$, ya que con la tolerancia por defecto el solver puede detenerse en una solución levemente subóptima.

---

### Preguntas

**(a) [15 pts.]** Formule un modelo de programación lineal entera que permita a la municipalidad decidir qué tres artistas se presentan cada noche y en qué recinto, de modo de maximizar el público total esperado respetando todas las condiciones descritas. Defina claramente conjuntos, parámetros y variables de decisión, y explique el significado de cada restricción.

Explique cómo incorpora la función de demanda en su modelo y por qué su modelo es lineal, a pesar de que la demanda de una noche no es la suma de las demandas de cada artista.

**(b) [10 pts.]** Implemente y resuelva el modelo de forma computacional. En caso de tener múltiples soluciones óptimas, considere aquella de menor costo total[^1]. Una vez resuelto, reporte respecto a su solución óptima:
* Los artistas y el recinto de cada noche, con su público esperado.
* El público total esperado y el costo total.
* Si se requiere el plan de seguridad.

*En lo consecutivo, consideraremos la situación modelada en (a) y resuelta en (b) como la situación base.*

**(c)** El año pasado, la artista principal del sábado canceló su presentación a última hora y el público de esa noche cayó a menos de un tercio de lo esperado. La municipalidad quiere evitar que algo así vuelva a ocurrir.
* **I. [5 pts.]** Para cada noche de su solución, determine cuánto público se esperaría si cancela cada uno de los tres artistas y se presentan solo los otros dos. Identifique qué noches dependen más de un solo artista.
* **II. [7 pts.]** A partir de su análisis, proponga una o más condiciones que hagan la parrilla menos dependiente de un solo artista. Incorpórelas al modelo, resuélvalo y compare las alternativas en términos de público y costo.
* **III. [3 pts.]** ¿Cuál recomendaría a la municipalidad? Justifique su respuesta considerando lo que se gana y lo que se pierde.

**(d)** El presupuesto de la municipalidad aún no está confirmado y podría ser recortado o ampliado.
* **I. [5 pts.]** Resuelva su modelo de (b) para presupuestos de $180$, $220$, $260$, $300$ y $340\text{ MM\$}$. Para cada caso, reporte el público total, el público y el recinto de cada noche, y si se requiere el plan de seguridad. Presente sus resultados en un gráfico.
* **II. [4 pts.]** ¿Qué noche queda más desmejorada? Explique por qué ocurre esto a partir de la formulación de su modelo.
* **III. [6 pts.]** Proponga una o más condiciones que permitan mejorar la situación de la noche más desmejorada sin aumentar el presupuesto de $250\text{ MM\$}$. Incorpórelas al modelo, resuélvalo y compare sus efectos sobre el público de cada noche y el público total.
* **IV. [5 pts.]** Para la condición que considere más adecuada, analice cómo cambian los resultados al variar su nivel de exigencia. ¿Cuánto público total se pierde por cada nivel? ¿Qué presupuesto adicional se requeriría para cumplir esa exigencia sin perder público total? A partir de su análisis, recomiende un nivel de exigencia y justifíquelo.

[^1]: Los criterios de desempate pueden ser implementados resolviendo modelos de manera secuencial, fijando en cada etapa el valor óptimo obtenido en la etapa anterior.