# 📋 PREGUNTAS DE SUSTENTACIÓN - SISTEMA GIMNASIO 3STARS SOLUTIONS

## 🎯 **TEMAS DEL CURSO EVALUADOS**
- **Programación Orientada a Objetos (POO)**
- **Arreglos con NumPy**
- **Persistencia de Archivos**
- **Diagramas de Clases**
- **Algoritmos y Estructuras de Datos**

---

## 🏗️ **1. PROGRAMACIÓN ORIENTADA A OBJETOS (POO)**

### **📚 Conceptos Fundamentales**

**P1.1:** ¿Cuáles son las 4 clases principales de tu sistema y explica la responsabilidad de cada una?
- **R:** `Gimnasio` (gestión principal), `Cliente` (información personal), `Membresia` (planes y pagos), `Entrenador` (personal especializado), `SesionEspecial` (eventos y actividades)

**P1.2:** En tu clase `Cliente`, identifica y explica los conceptos de:
- Encapsulación (atributos privados)
- Métodos getters y setters
- **R:** Atributos como `__id_cliente`, `__nombre`, `__documento` son privados. Métodos `get_nombre()`, `set_membresia()` para acceso controlado.

**P1.3:** ¿Qué es la encapsulación y cómo la implementaste en la clase `Membresia`?
- **R:** Usar `__pago`, `__fecha_inicio`, `__fecha_fin` como atributos privados, accesibles solo mediante métodos públicos.

**P1.4:** Explica la diferencia entre composición y agregación en tu diagrama de clases.
- **R:** Composición: `Gimnasio` contiene `Cliente` (rombo relleno). Agregación: `SesionEspecial` usa `Entrenador` (rombo vacío).

### **🔗 Relaciones entre Clases**

**P1.5:** ¿Qué tipo de relación existe entre `Cliente` y `Membresia`? ¿Por qué?
- **R:** Composición (1:1), porque un cliente puede tener máximo una membresía activa y la membresía depende del cliente.

**P1.6:** ¿Cómo implementaste la relación entre `SesionEspecial` y los clientes inscritos?
- **R:** Array NumPy `__inscritos` que almacena objetos `Cliente`, permitiendo múltiples inscripciones.

**P1.7:** ¿Por qué `Gimnasio` tiene una relación de composición con `Cliente` y no de agregación?
- **R:** Porque el gimnasio controla el ciclo de vida completo de los clientes (creación, modificación, eliminación).

### **🏭 Constructores y Métodos**

**P1.8:** Explica el constructor de la clase `Gimnasio`. ¿Qué parámetros recibe y cómo inicializa los arrays?
- **R:** Recibe nombre, dirección, teléfono, correo y efectivo. Inicializa array NumPy de clientes con `np.full(50, None)` y listas para entrenadores/sesiones.

**P1.9:** ¿Por qué algunos parámetros en los constructores tienen valores por defecto?
- **R:** Para hacer opcional ciertos datos (ej: `telefono=None`, `efectivo=0`, `pago=False`), mejorando la flexibilidad.

**P1.10:** ¿Qué validaciones implementaste en el método `crear_cliente()`?
- **R:** Validación de capacidad máxima, verificación de tipos de datos con `Utils`, comprobación de clientes duplicados.

---

## 🔢 **2. ARREGLOS CON NUMPY**

### **📊 Implementación con NumPy**

**P2.1:** ¿Por qué elegiste NumPy arrays para almacenar clientes en lugar de listas de Python?
- **R:** Eficiencia en memoria, acceso rápido por índices, tamaño fijo predefinido, mejor para búsquedas.

**P2.2:** Explica cómo funciona `np.full(self.__maximo_clientes, None, dtype=object)` en tu código.
- **R:** Crea array de tamaño fijo (50) lleno de `None`, tipo `object` para almacenar referencias a objetos `Cliente`.

**P2.3:** ¿Cómo implementaste la búsqueda de clientes en el array NumPy?
- **R:** Iteración por el array usando índices, comparando atributos como documento o ID hasta encontrar coincidencia.

**P2.4:** ¿Qué ventajas tiene usar `dtype=object` en tu array de clientes?
- **R:** Permite almacenar objetos Python completos (instancias de `Cliente`) en lugar de solo tipos primitivos.

### **🔍 Operaciones con Arrays**

**P2.5:** ¿Cómo manejas la eliminación de clientes del array NumPy sin redimensionarlo?
- **R:** Asignar `None` a la posición del cliente eliminado, mantener contador `__numero_clientes`.

**P2.6:** Explica el algoritmo que usas para encontrar una posición libre en el array de clientes.
- **R:** Iterar desde índice 0 hasta encontrar posición con valor `None`, usar esa posición para nuevo cliente.

**P2.7:** ¿Cómo implementaste el método `visualizar_clientes()` recorriendo el array?
- **R:** Bucle que verifica `if cliente is not None` para mostrar solo posiciones ocupadas del array.

**P2.8:** ¿Qué pasa si intentas agregar más clientes que la capacidad máxima del array?
- **R:** Se valida `__numero_clientes >= __maximo_clientes` y se muestra mensaje de error, evitando overflow.

### **📈 Gestión de Memoria**

**P2.9:** ¿Por qué usaste arrays NumPy para clientes pero listas Python para entrenadores y sesiones?
- **R:** Clientes tienen límite fijo conocido (50), entrenadores/sesiones son dinámicos sin límite definido.

**P2.10:** ¿Cómo optimizaste el uso de memoria en el array de clientes inscritos de `SesionEspecial`?
- **R:** Array fijo de 25 posiciones (cupos máximos), evita redimensionamientos dinámicos.

---

## 💾 **3. PERSISTENCIA DE ARCHIVOS**

### **📁 Formatos de Archivo**

**P3.1:** ¿Qué formatos de archivo implementaste y para qué tipo de datos cada uno?
- **R:** TXT para clientes (CSV), JSON para datos completos del gimnasio, TXT para entradas y caja.

**P3.2:** ¿Por qué elegiste JSON para exportar los datos completos del gimnasio?
- **R:** Mantiene estructura jerárquica, fácil de leer/escribir, compatible con otros sistemas, preserva tipos de datos.

**P3.3:** Explica la estructura del archivo `clientes.txt`. ¿Por qué usaste punto y coma como separador?
- **R:** Formato CSV con `;` para evitar conflictos con comas en datos, incluye información de membresía en línea.

**P3.4:** ¿Cómo manejas la persistencia de las fechas en los archivos?
- **R:** Formato string "YYYY-MM-DD", conversión con `datetime.strptime()` al cargar.

### **💿 Lectura y Escritura**

**P3.5:** Explica paso a paso el método `exportar_clientes()`.
- **R:** Crear encabezado CSV, iterar array clientes, escribir datos con separador `;`, manejar membresías opcionales.

**P3.6:** ¿Cómo implementaste `cargar_clientes()` para leer desde archivo TXT?
- **R:** Leer línea por línea, `split(';')` para separar campos, crear objetos `Cliente` y `Membresia`, agregar al array.

**P3.7:** ¿Qué validaciones implementas al cargar datos desde archivos?
- **R:** Verificar existencia de archivo, validar formato de líneas, verificar capacidad máxima, manejar errores de conversión.

**P3.8:** ¿Cómo generas nombres únicos para los archivos de respaldo diario?
- **R:** Concatenar fecha actual `date.today().strftime('%Y%m%d')` al nombre base del archivo.

### **🔄 Sincronización de Datos**

**P3.9:** ¿Cuándo se ejecuta automáticamente la exportación de datos?
- **R:** Al finalizar la aplicación mediante `exportar_datos_rapido()` en función `App()`.

**P3.10:** ¿Cómo aseguras que no se pierdan datos si el programa termina inesperadamente?
- **R:** Exportación manual disponible en menú, archivos de respaldo con fechas, validación antes de operaciones críticas.

---

## 🎨 **4. DIAGRAMAS DE CLASES**

### **🏗️ Estructura del Diagrama**

**P4.1:** Explica las relaciones mostradas en tu diagrama de clases `ClassDiagram.mmd`.
- **R:** 
  - `Gimnasio` → `Cliente` (composición 1:*)
  - `Cliente` → `Membresia` (composición 1:1)
  - `SesionEspecial` → `Cliente` (agregación *:*)
  - `SesionEspecial` → `Entrenador` (agregación 1:1)

**P4.2:** ¿Qué significan los símbolos de rombo relleno vs rombo vacío en tu diagrama?
- **R:** Rombo relleno = composición (ciclo de vida dependiente), rombo vacío = agregación (independencia de objetos).

**P4.3:** ¿Por qué `Cliente` tiene composición con `Membresia` y no agregación?
- **R:** Porque la membresía no puede existir sin un cliente, su ciclo de vida depende completamente del cliente.

**P4.4:** Explica la cardinalidad "1:*" entre `Gimnasio` y `Cliente`.
- **R:** Un gimnasio puede tener múltiples clientes (hasta 50), pero cada cliente pertenece a un solo gimnasio.

### **📋 Atributos y Métodos**

**P4.5:** ¿Por qué algunos atributos en tu diagrama tienen el símbolo "-" (guión)?
- **R:** Indica visibilidad privada, implementada en Python con doble guión bajo `__atributo`.

**P4.6:** ¿Qué métodos públicos ("+") son más importantes en cada clase?
- **R:** `Gimnasio`: crear/buscar/eliminar; `Cliente`: info_cliente/registrar_entrada; `Membresia`: renovar/calcular_dias.

**P4.7:** ¿Cómo se representa en tu diagrama el uso de NumPy arrays?
- **R:** `Np.ndarray~Cliente~ clientes` y `Np.ndarray~Cliente~ inscritos` especifican tipo de array y contenido.

**P4.8:** ¿Por qué separaste entrenadores y sesiones en un submódulo aparte?
- **R:** Cohesión funcional: entrenadores y sesiones están relacionados entre sí, diferentes responsabilidad que clientes/membresías.

### **🔄 Flujo de Datos**

**P4.9:** Traza el flujo cuando un cliente se inscribe a una sesión especial según tu diagrama.
- **R:** `Gimnasio.agendar_sesion()` → busca `Cliente` → busca `SesionEspecial` → `SesionEspecial.inscribir_cliente()`.

**P4.10:** ¿Cómo validas que las relaciones del diagrama se cumplen en el código?
- **R:** Verificaciones de tipos, validaciones de capacidad, manejo de referencias entre objetos.

---

## 🧠 **5. ALGORITMOS Y LÓGICA**

### **🔍 Algoritmos de Búsqueda**

**P5.1:** ¿Qué algoritmo de búsqueda implementaste para encontrar clientes? ¿Cuál es su complejidad?
- **R:** Búsqueda lineal O(n), recorre array hasta encontrar coincidencia por ID o documento.

**P5.2:** ¿Cómo optimizarías la búsqueda de clientes si tuvieras miles de registros?
- **R:** Usar diccionarios con ID como clave O(1), o implementar búsqueda binaria si están ordenados O(log n).

**P5.3:** Explica el algoritmo para validar que un cliente no está duplicado.
- **R:** Antes de crear, recorrer array completo comparando documento de identidad, retornar error si existe.

### **⚡ Validaciones y Control de Errores**

**P5.4:** ¿Qué validaciones implementaste en el módulo `Utils.py`?
- **R:** `is_number()`, `is_positive()`, `is_string()` para validar tipos de entrada, `valid_yes_no()` para confirmaciones.

**P5.5:** ¿Cómo manejas los errores cuando un archivo no existe al intentar cargar datos?
- **R:** Try-catch, verificar existencia con `os.path.exists()`, mostrar mensaje informativo y continuar ejecución.

**P5.6:** ¿Qué pasa si un usuario ingresa una fecha inválida?
- **R:** Validación con `datetime.strptime()` en try-catch, solicitar nueva entrada hasta obtener formato correcto.

### **🎛️ Control de Flujo**

**P5.7:** Explica la estructura del menú principal y cómo implementaste la navegación.
- **R:** Switch con `match-case`, bucle `while True`, validación de opciones, llamadas a submenús específicos.

**P5.8:** ¿Cómo implementaste la confirmación antes de eliminar un cliente?
- **R:** Función `valid_yes_no()` que valida entrada "si/no", bucle hasta respuesta válida, retorno booleano.

**P5.9:** ¿Qué patrón de diseño implementaste para organizar los menús?
- **R:** Patrón de menús jerárquicos, cada funcionalidad tiene su propio submenú, separación de responsabilidades.

---

## 💰 **6. ANÁLISIS FINANCIERO Y REPORTES**

### **📊 Cálculos Financieros**

**P6.1:** ¿Cómo calculas los ingresos totales del gimnasio?
- **R:** Suma de membresías pagadas + entradas únicas + sesiones especiales, usando constantes de `Utils.py`.

**P6.2:** Explica el algoritmo del método `seguimiento_membresias()`.
- **R:** Recorrer clientes, verificar estado de membresía, categorizar por activas/vencidas/pendientes de pago.

**P6.3:** ¿Qué información incluyes en el `reporte_diario()`?
- **R:** Clientes atendidos, ingresos del día, membresías vendidas, sesiones realizadas, estado de caja.

### **📈 Análisis de Datos**

**P6.4:** ¿Cómo determinas qué membresías están próximas a vencer?
- **R:** Método `calcular_dias_restantes()` de `Membresia`, filtrar las que tienen menos de 7 días.

**P6.5:** ¿Qué métricas consideras más importantes para el análisis del gimnasio?
- **R:** Tasa de renovación, ingresos por mes, ocupación promedio, clientes activos vs inactivos.

---

## 🛠️ **7. IMPLEMENTACIÓN TÉCNICA**

### **🔧 Decisiones de Diseño**

**P7.1:** ¿Por qué separaste las clases en diferentes archivos Python?
- **R:** Separación de responsabilidades, mantenibilidad, reutilización, organización lógica por funcionalidad.

**P7.2:** ¿Qué ventajas tiene usar constantes en `Utils.py` en lugar de números mágicos?
- **R:** Facilita mantenimiento, cambios centralizados, mejor legibilidad, reduce errores.

**P7.3:** ¿Cómo implementaste la validación de capacidad máxima del gimnasio?
- **R:** Contador `__numero_clientes` vs `__maximo_clientes`, verificación antes de agregar nuevos clientes.

### **🚀 Optimización y Rendimiento**

**P7.4:** ¿Qué estrategias usaste para optimizar el rendimiento con arrays grandes?
- **R:** Arrays de tamaño fijo, acceso directo por índice, evitar redimensionamientos dinámicos.

**P7.5:** ¿Cómo manejas la memoria cuando eliminas muchos clientes?
- **R:** Asignar `None` en lugar de reordenar array, mantener referencias claras, contador actualizado.

---

## 🎯 **8. PREGUNTAS INTEGRADORAS (MUY IMPORTANTES)**

**P8.1:** **Explica el ciclo completo desde que se registra un cliente hasta que paga su membresía, mencionando todas las clases involucradas.**

**P8.2:** **¿Cómo modificarías tu sistema para soportar múltiples gimnasios? ¿Qué cambios harías en el diagrama de clases?**

**P8.3:** **Si tuvieras que agregar un sistema de descuentos, ¿dónde y cómo lo implementarías sin romper el código existente?**

**P8.4:** **Explica cómo tu sistema garantiza la integridad de los datos entre la memoria (arrays NumPy) y los archivos de persistencia.**

**P8.5:** **¿Qué patrones de diseño identificas en tu código y cómo mejoran la calidad del software?**

---

## 📝 **CONSEJOS PARA LA SUSTENTACIÓN**

### **✅ Preparación Recomendada:**
1. **Practicar explicar el diagrama de clases** - Es lo que más preguntan
2. **Conocer bien las relaciones entre clases** - Composición vs Agregación
3. **Entender el uso de NumPy** - Por qué, cómo y cuándo
4. **Preparar ejemplos de persistencia** - Mostrar archivos reales
5. **Revisar validaciones y manejo de errores** - Casos límite

### **🎯 Puntos Clave a Enfatizar:**
- **POO:** Encapsulación, relaciones, responsabilidades de cada clase
- **NumPy:** Eficiencia, arrays fijos, gestión de memoria
- **Persistencia:** Múltiples formatos, integridad de datos, respaldos
- **Algoritmos:** Búsquedas, validaciones, complejidad temporal

### **⚠️ Errores Comunes a Evitar:**
- No saber explicar la diferencia entre composición y agregación
- Confundir el uso de arrays NumPy vs listas Python
- No poder explicar cómo funcionan las validaciones
- No entender el flujo de datos entre clases

---

**¡Éxito en tu sustentación! 🎓**
