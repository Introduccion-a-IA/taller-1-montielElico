# Taller 1 - Introducción a la Inteligencia Artificial
## Sistemas Expertos con Experta

---

## 📋 Descripción General

Este taller contiene **3 ejercicios** sobre sistemas expertos usando la librería `experta` en Python:

1. **Sistema Experto para Diagnóstico de Vehículos**
2. **Árbol Genealógico (Relaciones Familiares)**
3. **Sistema de Diagnóstico Médico**

---

## 🚀 Instrucciones Generales

### Paso 1: Acepta la asignación
Ya lo hiciste al obtener acceso a este repositorio.

### Paso 2: Descarga el notebook
Descarga el archivo `Taller_1.ipynb` y ábrelo en:
- **Google Colab** (recomendado)
- **Jupyter Notebook** local
- **VS Code** con extensión de Jupyter

### Paso 3: Completa los ejercicios
Busca y completa todas las partes marcadas con:
- `**` (asteriscos)
- `# Completar`
- `# Completa`

### Paso 4: Sube tu trabajo
Una vez completado:
```bash
git add Taller_1.ipynb
git commit -m "Completar Taller 1"
git push origin main
```

### Paso 5: Verifica tu calificación
1. Ve a la pestaña **"Actions"** en GitHub
2. Espera a que termine la ejecución (icono verde ✓ o rojo ✗)
3. Haz clic en la ejecución para ver tu puntuación detallada

---

## 📝 Detalles de los Ejercicios

### Ejercicio 1: Diagnóstico de Vehículos (100 pts)
**Objetivo:** Completar un sistema experto que diagnostica fallas en vehículos.

**Qué completar:**
- Regla de diagnóstico para frenos
- Regla de diagnóstico para refrigerante
- Regla de revisión general con operador `NOT`
- Declaraciones `self.declare()` para diagnósticos y acciones
- Declaraciones `self.retract()` para eliminar síntomas
- Sección de ejecución del motor

**Valores de salience:**
- Fallas graves: 100
- Diagnóstico moderado: 50-90
- Reparaciones: 150
- Revisión general: 10
- Verificación final: 5

---

### Ejercicio 2: Árbol Genealógico (100 pts)
**Objetivo:** Implementar reglas de inferencia para deducir relaciones familiares.

**Qué completar:**
- Reglas para inferir abuelos y abuelas
- Reglas para inferir hermanos y hermanas
- Reglas para inferir tíos y tías
- Reglas para inferir primos
- Control de relaciones procesadas para evitar duplicados

**Valores de salience:**
- Progenitores: 100
- Abuelos/abuelas: 80
- Hermanos/hermanas: 60
- Tíos/tías: 40
- Primos: 20

**Base de conocimiento proporcionada:**
- Familia con 10 personas (5 hombres, 5 mujeres)
- Relaciones de padre y madre ya definidas

---

### Ejercicio 3: Diagnóstico Médico (100 pts)
**Objetivo:** Crear un sistema experto que diagnostica enfermedades y genera recomendaciones.

**Qué completar:**
- Definición de clases `Fact` (Sintoma, Enfermedad, Diagnostico, etc.)
- Clase `DiagnosticoMedico(KnowledgeEngine)`
- Reglas de evaluación para 4 enfermedades:
  - Resfriado común
  - Gripe
  - COVID-19
  - Neumonía
- Reglas de recomendación según gravedad:
  - Leve (nivel 1): Descanso en casa
  - Moderada (nivel 2): Consultar al médico
  - Grave (nivel 3): Atención médica urgente

**Lógica de coincidencia:**
Si al menos la mitad de los síntomas coinciden, se declara el diagnóstico.

---

## 🎯 Criterios de Evaluación

### Distribución de Puntos (300 pts totales):

#### Ejercicio 1 (100 pts):
- Sintaxis correcta: 10 pts
- Regla de frenos: 20 pts
- Regla de refrigerante: 20 pts
- Uso de NOT: 15 pts
- Declaraciones declare(): 15 pts
- Declaraciones retract(): 10 pts
- Sección de ejecución: 10 pts

#### Ejercicio 2 (100 pts):
- Clases Fact definidas: 16 pts
- Regla de abuelo: 15 pts
- Regla de abuela: 15 pts
- Regla de hermano: 12 pts
- Regla de hermana: 12 pts
- Regla de tío: 10 pts
- Regla de tía: 10 pts
- Reglas de primos: 10 pts
- Sintaxis correcta: 10 pts

#### Ejercicio 3 (100 pts):
- Clases definidas: 20 pts
- Clase DiagnosticoMedico: 10 pts
- Reglas de evaluación (4): 40 pts
- Reglas de recomendación (3): 30 pts
- Sintaxis correcta: 10 pts

### Calificaciones:
- **Excelente**: ≥ 85% (255+ pts)
- **Bueno**: ≥ 70% (210+ pts)
- **Aceptable**: ≥ 60% (180+ pts)
- **Insuficiente**: < 60%

---

## ✨ Consejos Importantes

### General:
- Lee cuidadosamente los comentarios en el código
- Respeta la indentación de Python
- No elimines código ya existente
- Prueba tu código en Colab antes de subirlo

### Ejercicio 1:
- Los valores de `salience` determinan el orden de ejecución
- Usa `self.declare()` para agregar hechos
- Usa `self.retract()` para eliminar hechos

### Ejercicio 2:
- Evita comparar una persona consigo misma (`if hijo1 == hijo2: return`)
- Usa `relaciones_procesadas` para evitar duplicados
- Las reglas se ejecutan en cascada (progenitor → abuelo → primo)

### Ejercicio 3:
- Compara listas de síntomas correctamente
- La gravedad se usa para generar recomendaciones
- El sistema debe manejar cuando no se encuentra diagnóstico

---

## 🔍 Cómo Ver Resultados Detallados

1. **Durante la ejecución:** Ve a Actions → Click en la ejecución activa
2. **Ver logs:** Expande cada paso para ver detalles
3. **Descargar reporte:** En "Artifacts" descarga `resultados-calificacion`

El reporte incluye:
- Puntuación por ejercicio
- Checklist detallado de qué está completo y qué falta
- Mensajes de error específicos
- Porcentaje final

---

## 🆘 Solución de Problemas

### El workflow no se ejecuta:
- Verifica que subiste el archivo a la rama `main` o `master`
- Revisa que el archivo se llame exactamente `Taller_1.ipynb`

### Puntuación baja:
- Lee el reporte detallado en Actions
- Verifica que completaste TODAS las partes marcadas
- Asegúrate de que no haya errores de sintaxis

### Error de sintaxis:
- Verifica paréntesis y comillas cerrados
- Revisa la indentación (usa 4 espacios)
- Prueba el código celda por celda en Colab

### El código no compila:
- Busca `**` sin reemplazar
- Verifica nombres de variables correctos
- Asegúrate de completar todos los `# Completar`

---

## 📚 Recursos Adicionales

- [Documentación de Experta](https://experta.readthedocs.io/)
- [Python Docs](https://docs.python.org/3/)
- Consulta a tus profesores en caso de dudas conceptuales

---

## 📞 Contacto

Si tienes problemas técnicos con:
- **GitHub Classroom:** Contacta a tus profesores
- **El código:** Revisa el material de clase
- **La lógica:** Consulta el enunciado del taller

---

**¡Buena suerte con tu taller! 🎓**

**Fecha límite:** 
**Calificación automática:** Inmediata al hacer push
