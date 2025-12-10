# Charla Glitching == Hardware Hacking ES


---
### Introducción
### Teoría de Ataques de canal paralelo
#### Glitch de Tensión
#### Glitch de Reloj
#### Ataques de Power Analisis
---

### Introducción


Los ataques de canal paralelo se suelen referir con el acrónimo SCA (Side Channel Attack).

Son una clase de ataques de ciberseguridad que se centran en cambiar el hilo
de computación de un sistema revisando las implementaciones físicas en lugar
de atacar la fortaleza matemática del algoritmo en sí.

Los intentos de analizar los efectos del glitching en el hardware están 
sujetos al efecto Heisenberg, por lo cual, al "introducir una sonda de medición"
estamos alterando automáticamente el medio físico del sistema estudiado.


===

### Teoría de los ataques de canal paralelo

Los ataques de canal paralelo persiguen forzar un fallo buscando un defecto hardware, y no un defecto en el software.

| Tipo de Ataque | Medida Colateral Explotada | Ejemplo de Información Inferencia |
| :--- | :--- | :--- |
| **Ataques de Sincronización (Timing Attacks)** | Tiempo que tarda el dispositivo en realizar distintas operaciones (cálculos, comparaciones, accesos a memoria). | Puede revelar la clave secreta al inferir qué operaciones se realizan más rápido o más lento dependiendo de los bits de la clave. |
| **Análisis de Consumo de Energía (Power Analysis)** | Variaciones en el consumo de energía eléctrica del dispositivo mientras realiza operaciones. | **DPA (Differential Power Analysis)** y **SPA (Simple Power Analysis)** correlacionan los picos de consumo con el procesamiento de bits específicos de la clave.  |
| **Análisis de Radiación Electromagnética (EM)** | Ondas de radio o campos electromagnéticos emitidos durante el procesamiento. | Permite deducir claves o textos planos al ser una manifestación física de la actividad interna. |
| **Ataques Acústicos** | Sonidos generados por los componentes (como bobinas o condensadores) durante el procesamiento de datos. | Se ha demostrado que pueden revelar claves criptográficas al analizar los patrones sonoros. |
| **Ataques de Caché (Cache Attacks)** | El atacante monitoriza los patrones de acceso a la memoria caché de la víctima en un sistema compartido. | Infiere qué datos están siendo procesados por la víctima al observar qué líneas de caché son usadas o desalojadas. |
| **Análisis de Fallos (Fault Analysis)** | Introduce fallos intencionados (ej. picos de voltaje, láseres) para que el cálculo criptográfico devuelva un resultado erróneo. | Ataque de Fallos Diferenciales (DFA) para deducir la clave. |

Los ataques de canal lateral a menudo requieren el uso de técnicas estadísticas avanzadas para extraer la información útil del "ruido" de la medición.

Correlación: Es la técnica central. El atacante realiza múltiples mediciones del canal lateral (ej. consumo de energía) mientras el sistema procesa diferentes entradas (ej. textos planos). Luego, intenta correlacionar las mediciones con las operaciones internas que se realizarían si la clave secreta fuera una clave conjeturada. La clave que muestre la correlación más alta es probablemente la correcta.

Análisis Diferencial: Se utiliza para amplificar las pequeñas diferencias en las mediciones que son causadas por la operación de bits específicos de la clave.

## ⚡ Glitch de Tensión

### 1. Marco Teórico: Inyección de Fallos

Un *crowbar glitch* se basa en el principio de la **Inyección de Fallos (Fault Injection - FI)**. El objetivo es obligar a un dispositivo a desviarse de su comportamiento intencionado mediante la alteración de su entorno físico o eléctrico.

* **Objetivo computacional:** Obligar al procesador a saltarse o ejecutar mal una instrucción clave (como una comparación de claves) o a producir un resultado criptográfico incorrecto del que se pueda inferir la clave secreta.
* **Objetivo de Seguridad:** Burlar mecanismos de protección de *hardware* o *software*, como verificaciones de contraseña, *checksums*, o la inicialización de estado de seguridad.

### 2. El Mecanismo "Crowbar" Glitch

El término "*crowbar*" se utiliza porque la técnica **cortocircuita o sobrecarga momentáneamente la línea de alimentación eléctrica** del circuito integrado (CI) objetivo.

#### **Funcionamiento Físico del Ataque**

1.  **Monitoreo Preciso:** Se identifica el **momento crítico (critical window)** en el que se ejecuta una instrucción sensible.
2.  **Activación del Glitch:** Un circuito de conmutación muy rápido (a menudo un MOSFET) es activado para **cortocircuitar la línea de voltaje VCC a tierra (GND)** por un periodo extremadamente corto (picosegundos a nanosegundos). 
3.  **El Efecto Eléctrico:** Este cortocircuito momentáneo provoca una **caída brusca e inmediata del voltaje de alimentación (VCC)** del chip.
4.  **El Efecto Lógico (El Fallo):** La caída de voltaje perturba el funcionamiento de los circuitos lógicos:
    * **Violación de Sincronización (Setup/Hold Time Violation):** Las celdas lógicas no reciben suficiente voltaje para cambiar su estado correctamente.
    * **Corrupción de Datos:** Los datos se corrompen en la memoria o en tránsito.
    * **Salto de Instrucción (Instruction Skip):** El procesador puede ejecutar mal o saltarse la instrucción que se estaba ejecutando, alterando el flujo del programa.


![Crowbar Glitch](02-img/glitch-voltabe_keysight.png "Glitch de tensión.")


### 3. Parámetros Críticos del Ataque

El éxito depende de la manipulación precisa de tres parámetros:

1.  **Tiempo (Timing):** El factor más crítico, requiere precisión de nanosegundos para golpear la instrucción deseada.
2.  **Duración (Width):** El tiempo que dura el cortocircuito. Si es muy corto, no causa fallo; si es muy largo, reinicia el dispositivo.
3.  **Amplitud (Magnitude):** La cantidad de corriente que se desvía, determinando la magnitud de la caída de voltaje.
4.  **Número de repeticiones (Repeats):** cantidad de cortocircuitos necesarios para saltar una instrucción. 

### 4. Usos Comunes del Crowbar Glitch

* **Bypass de Comprobaciones:** Forzar que una comprobación de clave o PIN siempre resulte verdadera.
* **Inyección de Códigos de Operación (Opcode Injection):** Inducir un fallo para que el procesador ejecute una instrucción diferente (ej. un `NOP` o un salto).
* **Ataque DFA Mejorado:** Generar un texto cifrado con un fallo preciso para usar el **Análisis Diferencial de Fallos (DFA)** y deducir la clave.

### 🛡️ Contramedidas

Las defensas se centran en la inmunidad del *hardware* a las fluctuaciones:

* **Filtros de Voltaje:** Agregar condensadores de desacoplo de alta frecuencia cerca de los puntos sensibles.
* **Monitores de Voltaje (Voltage Detectors):** Circuitos que detectan si el VCC cae por debajo de un umbral seguro y activan un reinicio instantáneo (*reset*).
* **Redundancia Temporal/Espacial:** Ejecutar operaciones críticas varias veces y comparar resultados.