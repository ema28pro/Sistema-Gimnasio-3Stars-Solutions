# 📋 PREGUNTAS DE SUSTENTACIÓN - SISTEMA GIMNASIO 3STARS SOLUTIONS

## 🎯 **TEMAS DEL CURSO EVALUADOS**
- Programación Orientada a Objetos (POO)
- Algoritmos de Búsqueda y Ordenamiento
- Eliminación con NumPy
- Persistencia de Archivos
- Diagramas de Clases

---

## 🏗️ **1. PROGRAMACIÓN ORIENTADA A OBJETOS (POO)**

### **Conceptos Fundamentales**

**P1.1:** ¿Cuáles son las 4 clases principales de tu sistema y explica la responsabilidad de cada una?

**P1.2:** En tu clase `Cliente`, identifica y explica los conceptos de:
- Encapsulación (atributos privados)
- Métodos getters y setters
- ¿Por qué los atributos están marcados como privados con `__`?

**P1.3:** ¿Cómo implementaste el principio de **responsabilidad única** en tu diseño? Da ejemplos específicos.

**P1.4:** Explica la diferencia entre composición y agregación en tu sistema. ¿Dónde aplicaste cada una?

### **Herencia y Polimorfismo**

**P1.5:** Tu sistema no usa herencia explícita. ¿En qué casos sería útil implementar herencia? Por ejemplo, ¿cómo crearías diferentes tipos de membresías (Básica, Premium, VIP)?

**P1.6:** Si tuvieras que implementar diferentes tipos de entrenadores (EntrenadorBoxeo, EntrenadorYoga), ¿cómo aplicarías polimorfismo?

### **Métodos y Constructores**

**P1.7:** En la clase `Membresia`, explica paso a paso qué hace el método `renovar_membresia()`. ¿Qué validaciones implementa?

**P1.8:** ¿Por qué el constructor de `Cliente` recibe `fecha_registro` como parámetro en lugar de generarla automáticamente?

---

## 🔍 **2. ALGORITMOS DE BÚSQUEDA**

### **Implementaciones de Búsqueda**

**P2.1:** En el método `buscar_cliente()` de la clase `Gimnasio`, describe los 3 tipos de búsqueda implementados y su complejidad temporal.

**P2.2:** ¿Qué tipo de búsqueda usas para encontrar un cliente por ID vs por documento? ¿Por qué?

**P2.3:** En el método `buscar_entrenador()`, ¿cómo optimizarías la búsqueda si tuvieras 1000 entrenadores?

**P2.4:** Explica cómo funciona la búsqueda en el método `sesiones_agendadas()` para un cliente específico.

### **Eficiencia y Optimización**

**P2.5:** Tu array de clientes usa búsqueda lineal. ¿En qué casos sería mejor usar búsqueda binaria? ¿Qué cambios necesitarías?

**P2.6:** ¿Cómo implementarías una búsqueda por nombre aproximada (fuzzy search) para casos donde el usuario no recuerda el nombre exacto?

---

## 📊 **3. ALGORITMOS DE ORDENAMIENTO**

### **Implementación Actual**

**P3.1:** ¿Dónde aplicas ordenamiento en tu sistema actual? ¿Usas métodos nativos de Python o NumPy?

**P3.2:** Si tuvieras que mostrar los clientes ordenados por fecha de registro, ¿qué algoritmo de ordenamiento implementarías y por qué?

**P3.3:** Para ordenar las membresías por días restantes, ¿usarías ordenamiento por burbuja, quicksort o mergesort? Justifica tu respuesta.

### **Casos Prácticos**

**P3.4:** Implementa pseudocódigo para ordenar las sesiones especiales por:
- Fecha (más próximas primero)
- Número de cupos disponibles
- Popularidad (más inscritos primero)

**P3.5:** ¿Cómo ordenarías los reportes financieros por mes/día para análisis temporal?

---

## 🗑️ **4. ELIMINACIÓN CON NUMPY**

### **Manejo de Arrays NumPy**

**P4.1:** En tu clase `Gimnasio`, el array `__clientes` usa NumPy. Explica:
- ¿Por qué usaste `np.full()` en lugar de una lista normal?
- ¿Cómo manejas la eliminación lógica vs física?

**P4.2:** En el método `eliminar_cliente()`, ¿cómo reorganizas el array después de eliminar un elemento? ¿Dejas espacios vacíos?

**P4.3:** En `SesionEspecial`, el array `__inscritos` usa NumPy. Explica el proceso de eliminación en `editar_inscritos()`.

### **Ventajas de NumPy**

**P4.4:** ¿Qué ventajas ofrece NumPy sobre las listas de Python para tu sistema de gimnasio?

**P4.5:** ¿Cómo manejas la fragmentación del array cuando eliminas elementos del medio?

**P4.6:** Si tuvieras que eliminar múltiples clientes a la vez, ¿cómo optimizarías el proceso?

---

## 💾 **5. PERSISTENCIA DE ARCHIVOS**

### **Formatos y Estructura**

**P5.1:** Tu sistema usa archivos `.txt` y `.json`. Explica:
- ¿Cuándo usas cada formato y por qué?
- Ventajas y desventajas de cada uno

**P5.2:** En el archivo `clientes.txt`, ¿por qué usaste `;` como separador en lugar de `,`?

**P5.3:** Explica la estructura del archivo JSON que exportas con `exportar_datos_json()`.

### **Operaciones de Archivo**

**P5.4:** En el método `cargar_clientes()`, explica paso a paso:
- Cómo lees el archivo
- Cómo parseas cada línea
- Cómo manejas errores de formato

**P5.5:** ¿Cómo implementaste el respaldo automático de datos? ¿Qué pasa si el programa se cierra inesperadamente?

**P5.6:** En `registrar_entrada()`, ¿por qué usas modo "append" (`"a"`) en lugar de reescribir el archivo completo?

### **Integridad de Datos**

**P5.7:** ¿Cómo validás que los datos cargados desde archivo sean consistentes?

**P5.8:** ¿Qué estrategia usas para evitar pérdida de datos durante las operaciones de escritura?

---

## 📐 **6. DIAGRAMA DE CLASES**

### **Análisis del Diagrama**

**P6.1:** En tu diagrama de clases (`ClassDiagram.mmd`), explica:
- Las relaciones entre `Gimnasio` y `Cliente`
- ¿Es composición o agregación? ¿Por qué?

**P6.2:** ¿Por qué la relación entre `Cliente` y `Membresia` es composición (rombo relleno)?

**P6.3:** Explica la relación entre `SesionEspecial`, `Cliente` y `Entrenador`.

### **Cardinalidades**

**P6.4:** Justifica las cardinalidades:
- Gimnasio 1 → 0..* Cliente
- Cliente 1 → 1 Membresia
- SesionEspecial 1 → 0..* Cliente

**P6.5:** ¿Qué cambiarías en el diagrama si un cliente pudiera tener múltiples membresías activas?

### **Métodos en el Diagrama**

**P6.6:** ¿Por qué algunos métodos aparecen en el diagrama y otros no? ¿Cuál es el criterio?

**P6.7:** Si tuvieras que agregar una clase `Pago`, ¿dónde la ubicarías en el diagrama y con qué relaciones?

---

## 🚀 **7. PREGUNTAS INTEGRADORAS**

### **Arquitectura del Sistema**

**P7.1:** Explica el flujo completo desde que un cliente se registra hasta que paga su primera mensualidad.

**P7.2:** ¿Cómo manejas la concurrencia si dos usuarios intentan registrar el mismo cliente simultáneamente?

**P7.3:** Describe cómo implementaste el patrón MVC (Model-View-Controller) en tu sistema.

### **Escalabilidad y Mejoras**

**P7.4:** Si el gimnasio crece a 10,000 clientes, ¿qué cambios harías en:
- Estructura de datos
- Algoritmos de búsqueda
- Persistencia de archivos

**P7.5:** ¿Cómo migrarías tu sistema de archivos a una base de datos relacional?

**P7.6:** Propón 3 nuevas funcionalidades y explica cómo las implementarías sin romper el diseño actual.

### **Mantenimiento y Testing**

**P7.7:** ¿Cómo validás que tu sistema funciona correctamente? ¿Qué casos de prueba implementarías?

**P7.8:** ¿Qué estrategias usas para el manejo de errores y excepciones?

---

## 🎯 **8. PREGUNTAS ESPECÍFICAS DEL CÓDIGO**

### **Análisis de Main.py**

**P8.1:** En la función `menu()`, ¿por qué usas `match-case` en lugar de `if-elif`? ¿Cuáles son las ventajas?

**P8.2:** Explica la función `exportar_datos_rapido()` y su propósito en el flujo del programa.

### **Utils.py**

**P8.3:** En `Utils.py`, explica las funciones de validación:
- `is_number()`, `is_positive()`, `is_string()`
- ¿Por qué separaste las validaciones en funciones independientes?

### **Gestión de Memoria**

**P8.4:** ¿Cómo manejas la memoria cuando el array de clientes está lleno pero quieres agregar más?

**P8.5:** ¿Qué estrategia usas para evitar memory leaks en arrays grandes?

---

## 🏆 **9. PREGUNTAS AVANZADAS**

### **Complejidad Algorítmica**

**P9.1:** Calcula la complejidad temporal Big O de:
- Buscar un cliente por ID
- Eliminar un cliente
- Cargar todos los clientes desde archivo

**P9.2:** ¿Cuál es la complejidad espacial de tu sistema con N clientes?

### **Patrones de Diseño**

**P9.3:** Identifica qué patrones de diseño aplicaste (Factory, Singleton, Observer, etc.)

**P9.4:** ¿Cómo implementarías el patrón Strategy para diferentes tipos de descuentos en membresías?

### **Optimización**

**P9.5:** Si tuvieras que optimizar el sistema para funcionar en un dispositivo con memoria limitada, ¿qué cambios harías?

**P9.6:** Propón una estrategia de caché para mejorar el rendimiento de las búsquedas frecuentes.

---

## 📚 **10. TIPS PARA LA SUSTENTACIÓN**

### **Preparación Recomendada:**

1. **Conoce tu código:** Revisa cada clase y método, entiende qué hace y por qué
2. **Practica explicar:** Usa diagramas en pizarra para explicar relaciones
3. **Prepara ejemplos:** Ten casos específicos para cada concepto
4. **Anticipa cambios:** Piensa cómo mejorarías o escalarías el sistema
5. **Domina el diagrama:** Es el corazón de la POO, explica cada relación

### **Frases Clave para Usar:**

- "Implementé encapsulación mediante..."
- "La complejidad temporal de este algoritmo es..."
- "Usé composición porque el objeto no puede existir independientemente..."
- "Para optimizar la búsqueda, implementé..."
- "La persistencia garantiza que los datos..."

---

## ✅ **CHECKLIST FINAL**

- [ ] Puedo explicar cada clase y sus responsabilidades
- [ ] Entiendo todas las relaciones del diagrama de clases
- [ ] Sé justificar las decisiones de diseño (POO, algoritmos, estructuras)
- [ ] Puedo proponer mejoras y optimizaciones
- [ ] Domino los conceptos de complejidad temporal y espacial
- [ ] Entiendo cómo funciona la persistencia de datos
- [ ] Puedo explicar el flujo completo del programa

---

**¡ÉXITO EN TU SUSTENTACIÓN! 🚀**

> **Recuerda:** La clave está en demostrar que entiendes no solo CÓMO funciona tu código, sino también POR QUÉ tomaste cada decisión de diseño.
