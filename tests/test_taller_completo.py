# tests/test_taller_estricto.py
import json
import sys
import re
from io import StringIO

class TallerEstrictoTester:
    def __init__(self, notebook_path):
        self.notebook_path = notebook_path
        self.score = 0
        self.max_score = 300
        self.results = []
        
    def load_notebook(self):
        """Carga el notebook y separa por ejercicios"""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            ejercicios = {'1': [], '2': [], '3': []}
            ejercicio_actual = None
            
            for cell in notebook['cells']:
                if cell['cell_type'] == 'markdown':
                    source = ''.join(cell['source'])
                    if '# Ejercicio 1' in source:
                        ejercicio_actual = '1'
                    elif '# Ejercicio 2' in source:
                        ejercicio_actual = '2'
                    elif '# Ejercicio 3' in source:
                        ejercicio_actual = '3'
                elif cell['cell_type'] == 'code' and ejercicio_actual:
                    source = ''.join(cell['source'])
                    if not source.strip().startswith('pip install') and 'collections.abc' not in source:
                        ejercicios[ejercicio_actual].append(source)
            
            return ejercicios
        except Exception as e:
            self.results.append(f"ERROR: No se pudo cargar el notebook: {e}")
            return None

    def check_incomplete_code(self, code):
        """Verifica si el código está incompleto"""
        issues = []
        
        # Buscar marcadores de código incompleto
        if '**' in code:
            issues.append("Contiene marcadores '**' sin completar")
        
        if '# Completar' in code or '# Completa' in code:
            issues.append("Contiene comentarios '# Completar' sin resolver")
        
        return issues

    def test_syntax(self, code, ejercicio_num):
        """Verifica sintaxis - si falla, retorna 0 puntos para ese ejercicio"""
        try:
            compile(code, f'<ejercicio{ejercicio_num}>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    # ========== EJERCICIO 1 ==========
    def test_ejercicio1(self, code):
        """Test estricto para ejercicio 1"""
        self.results.append("\n=== EJERCICIO 1: Sistema Experto Vehículos ===")
        points = 0
        
        # 1. Verificar código incompleto
        incomplete = self.check_incomplete_code(code)
        if incomplete:
            self.results.append(f"CÓDIGO INCOMPLETO:")
            for issue in incomplete:
                self.results.append(f"  ❌ {issue}")
            self.results.append("PUNTUACIÓN: 0/100 - Completa el código antes de evaluar")
            return 0
        
        # 2. Verificar sintaxis PRIMERO
        syntax_ok, error = self.test_syntax(code, 1)
        if not syntax_ok:
            self.results.append(f"❌ {error}")
            self.results.append("PUNTUACIÓN: 0/100 - Corrige los errores de sintaxis")
            return 0
        
        self.results.append("✅ Sintaxis correcta (10 pts)")
        points += 10
        
        # 3. Verificar estructura básica
        if 'class VehicleDiagnosis(KnowledgeEngine):' not in code:
            self.results.append("❌ Falta clase VehicleDiagnosis")
            return points
        
        # 4. Verificar regla de frenos COMPLETADA (no la de ejemplo)
        # Debe tener el decorador Y la función definida
        frenos_rule = re.search(r'@Rule\(Symptom\(tipo=[\'"]ruido_metalico[\'"]\),\s*salience=\d+\)\s*def\s+\w+\(self\):', code)
        if frenos_rule:
            # Verificar que tenga el cuerpo completo
            if 'Revisar_sistema_de_frenos' in code and "self.declare(Diagnosis(resultado=" in code:
                points += 20
                self.results.append("✅ Regla de frenos completada correctamente (20 pts)")
            else:
                self.results.append("❌ Regla de frenos incompleta (falta cuerpo)")
        else:
            self.results.append("❌ Regla de frenos no encontrada o mal formada")
        
        # 5. Verificar regla de refrigerante
        refrig_rule = re.search(r'@Rule\(AND\(.*Symptom\(tipo=[\'"]fuga_liquido[\'"].*CarState\(estado=[\'"]motor_caliente[\'"].*\),\s*salience=\d+\)', code)
        if refrig_rule:
            if 'Perdida_de_refrigerante' in code:
                points += 20
                self.results.append("✅ Regla de refrigerante completada (20 pts)")
        else:
            self.results.append("❌ Regla de refrigerante incompleta")
        
        # 6. Verificar uso de NOT en revisión general
        not_rule = re.search(r'@Rule\(NOT\(Symptom.*NOT\(Symptom.*NOT\(Symptom', code)
        if not_rule:
            points += 15
            self.results.append("✅ Regla con NOT implementada (15 pts)")
        else:
            self.results.append("❌ Regla de revisión general sin NOT correctos")
        
        # 7. Verificar declares (debe haber varios)
        declare_count = code.count('self.declare(Diagnosis(')
        declare_count += code.count('self.declare(RepairAction(')
        declare_count += code.count('self.declare(VehicleStatus(')
        
        if declare_count >= 10:
            points += 15
            self.results.append(f"✅ Declaraciones declare() completas ({declare_count}) (15 pts)")
        else:
            self.results.append(f"⚠️ Pocas declaraciones ({declare_count}/10 esperadas)")
        
        # 8. Verificar retracts
        retract_count = code.count('self.retract(fact)')
        if retract_count >= 3:
            points += 10
            self.results.append(f"✅ Declaraciones retract() correctas ({retract_count}) (10 pts)")
        else:
            self.results.append(f"❌ Faltan declaraciones retract() ({retract_count}/3)")
        
        # 9. Verificar sección de ejecución
        has_engine = 'engine = VehicleDiagnosis()' in code
        has_reset = 'engine.reset()' in code
        has_run = 'engine.run()' in code
        has_declares = 'engine.declare(Symptom(' in code
        
        exec_points = 0
        if has_engine:
            exec_points += 3
        if has_reset:
            exec_points += 3
        if has_run:
            exec_points += 4
        if has_declares:
            symptom_count = code.count('engine.declare(Symptom(')
            if symptom_count >= 2:
                exec_points += 5
        
        if exec_points >= 12:
            points += exec_points
            self.results.append(f"✅ Sección de ejecución completa ({exec_points} pts)")
        else:
            self.results.append(f"⚠️ Sección de ejecución incompleta ({exec_points}/15 pts)")
        
        self.results.append(f"\n📊 TOTAL EJERCICIO 1: {points}/100")
        return points

    # ========== EJERCICIO 2 ==========
    def test_ejercicio2(self, code):
        """Test estricto para ejercicio 2"""
        self.results.append("\n=== EJERCICIO 2: Árbol Genealógico ===")
        points = 0
        
        # 1. Verificar código incompleto
        incomplete = self.check_incomplete_code(code)
        if incomplete:
            self.results.append("CÓDIGO INCOMPLETO:")
            for issue in incomplete:
                self.results.append(f"  ❌ {issue}")
            self.results.append("PUNTUACIÓN: 0/100")
            return 0
        
        # 2. Sintaxis
        syntax_ok, error = self.test_syntax(code, 2)
        if not syntax_ok:
            self.results.append(f"❌ {error}")
            self.results.append("PUNTUACIÓN: 0/100")
            return 0
        
        self.results.append("✅ Sintaxis correcta (10 pts)")
        points += 10
        
        # 3. Verificar clases Fact
        required_classes = ['Progenitor', 'Abuelo', 'Abuela', 'Hermano', 'Hermana', 'Tio', 'Tia', 'Primo']
        class_points = 0
        for cls in required_classes:
            if f'class {cls}(Fact):' in code:
                class_points += 2
        
        if class_points >= 14:
            points += 16
            self.results.append(f"✅ Clases Fact definidas ({len(required_classes)}) (16 pts)")
        else:
            self.results.append(f"⚠️ Faltan clases ({class_points}/16 pts)")
        
        # 4. Verificar reglas completadas (buscar self.declare dentro de funciones específicas)
        
        # Abuelo
        if 'def inferir_abuelo' in code and 'self.declare(Abuelo(abuelo=' in code:
            points += 12
            self.results.append("✅ Regla de abuelo completada (12 pts)")
        else:
            self.results.append("❌ Regla de abuelo incompleta")
        
        # Abuela
        if 'def inferir_abuela' in code and 'self.declare(Abuela(abuela=' in code:
            points += 12
            self.results.append("✅ Regla de abuela completada (12 pts)")
        else:
            self.results.append("❌ Regla de abuela incompleta")
        
        # Hermano
        if 'def inferir_hermano' in code and 'self.declare(Hermano(hermano=' in code:
            points += 10
            self.results.append("✅ Regla de hermano completada (10 pts)")
        else:
            self.results.append("❌ Regla de hermano incompleta")
        
        # Hermana
        if 'def inferir_hermana' in code and 'self.declare(Hermana(hermana=' in code:
            points += 10
            self.results.append("✅ Regla de hermana completada (10 pts)")
        else:
            self.results.append("❌ Regla de hermana incompleta")
        
        # Tío
        if 'def inferir_tio' in code and 'self.declare(Tio(tio=' in code:
            points += 10
            self.results.append("✅ Regla de tío completada (10 pts)")
        else:
            self.results.append("❌ Regla de tío incompleta")
        
        # Tía
        if 'def inferir_tia' in code and 'self.declare(Tia(tia=' in code:
            points += 10
            self.results.append("✅ Regla de tía completada (10 pts)")
        else:
            self.results.append("❌ Regla de tía incompleta")
        
        # Primos
        primo_declares = code.count('self.declare(Primo(primo=')
        if primo_declares >= 4:  # Debe haber múltiples declaraciones
            points += 10
            self.results.append("✅ Reglas de primos completadas (10 pts)")
        else:
            self.results.append(f"❌ Reglas de primos incompletas ({primo_declares}/4 declares)")
        
        self.results.append(f"\n📊 TOTAL EJERCICIO 2: {points}/100")
        return points

    # ========== EJERCICIO 3 ==========
    def test_ejercicio3(self, code):
        """Test estricto para ejercicio 3"""
        self.results.append("\n=== EJERCICIO 3: Diagnóstico Médico ===")
        points = 0
        
        # 1. Verificar código incompleto
        incomplete = self.check_incomplete_code(code)
        if incomplete:
            self.results.append("CÓDIGO INCOMPLETO:")
            for issue in incomplete:
                self.results.append(f"  ❌ {issue}")
            self.results.append("PUNTUACIÓN: 0/100")
            return 0
        
        # 2. Sintaxis
        syntax_ok, error = self.test_syntax(code, 3)
        if not syntax_ok:
            self.results.append(f"❌ {error}")
            self.results.append("PUNTUACIÓN: 0/100")
            return 0
        
        self.results.append("✅ Sintaxis correcta (10 pts)")
        points += 10
        
        # 3. Verificar clases base
        required_classes = ['Sintoma', 'Enfermedad', 'Gravedad', 'Diagnostico', 'Recomendacion']
        for cls in required_classes:
            if f'class {cls}(Fact):' in code:
                points += 4
        
        if points >= 30:
            self.results.append(f"✅ Clases Fact definidas (20 pts)")
        else:
            self.results.append(f"⚠️ Faltan clases ({(points-10)*5}/5)")
        
        # 4. Clase principal
        if 'class DiagnosticoMedico(KnowledgeEngine):' in code:
            points += 10
            self.results.append("✅ Clase DiagnosticoMedico definida (10 pts)")
        else:
            self.results.append("❌ Falta clase DiagnosticoMedico")
        
        # 5. Reglas de evaluación
        eval_methods = [
            ('evaluar_resfriado', 'resfriado_comun'),
            ('evaluar_gripe', 'gripe'),
            ('evaluar_covid', 'covid_19'),
            ('evaluar_neumonia', 'neumonia')
        ]
        
        for method_name, enfermedad in eval_methods:
            if f'def {method_name}' in code and f"enfermedad='{enfermedad}'" in code:
                points += 10
                self.results.append(f"✅ Método {method_name} implementado (10 pts)")
            else:
                self.results.append(f"❌ Método {method_name} incompleto")
        
        # 6. Reglas de recomendación
        rec_methods = [
            ('recomendar_leve', 'nivel=1'),
            ('recomendar_moderada', 'nivel=2'),
            ('recomendar_grave', 'nivel=3')
        ]
        
        for method_name, nivel in rec_methods:
            if f'def {method_name}' in code and nivel in code:
                points += 10
                self.results.append(f"✅ Método {method_name} implementado (10 pts)")
            else:
                self.results.append(f"❌ Método {method_name} incompleto")
        
        self.results.append(f"\n📊 TOTAL EJERCICIO 3: {points}/100")
        return points

    def run_tests(self):
        """Ejecuta todos los tests"""
        ejercicios = self.load_notebook()
        if not ejercicios:
            self.generate_report()
            return
        
        # Test cada ejercicio
        if ejercicios['1']:
            code1 = '\n\n'.join(ejercicios['1'])
            self.score += self.test_ejercicio1(code1)
        else:
            self.results.append("\n❌ EJERCICIO 1: No se encontró código")
        
        if ejercicios['2']:
            code2 = '\n\n'.join(ejercicios['2'])
            self.score += self.test_ejercicio2(code2)
        else:
            self.results.append("\n❌ EJERCICIO 2: No se encontró código")
        
        if ejercicios['3']:
            code3 = '\n\n'.join(ejercicios['3'])
            self.score += self.test_ejercicio3(code3)
        else:
            self.results.append("\n❌ EJERCICIO 3: No se encontró código")
        
        self.generate_report()
    
    def generate_report(self):
        """Genera reporte final"""
        percentage = (self.score / self.max_score) * 100
        
        if percentage >= 85:
            nivel = "EXCELENTE"
        elif percentage >= 70:
            nivel = "BUENO"
        elif percentage >= 60:
            nivel = "ACEPTABLE"
        else:
            nivel = "INSUFICIENTE"
        
        report = f"""
{'='*70}
RESULTADOS AUTOCALIFICACIÓN - TALLER 1 IA
{'='*70}

PUNTUACIÓN TOTAL: {self.score}/{self.max_score} ({percentage:.1f}%)
NIVEL: {nivel}

DETALLES POR EJERCICIO:
{chr(10).join(self.results)}

{'='*70}
CRITERIOS DE APROBACIÓN:
- Excelente:    >= 85% (255 pts)
- Bueno:        >= 70% (210 pts)  
- Aceptable:    >= 60% (180 pts)
- Insuficiente: <  60%
{'='*70}

NOTA: Este test verifica que el código esté COMPLETO (sin '**' ni 
'# Completar'), que compile sin errores, y que contenga las estructuras
requeridas. Si tienes 0 puntos en un ejercicio, revisa:
  1. ¿Completaste todos los espacios en blanco?
  2. ¿El código compila sin errores?
  3. ¿Seguiste las instrucciones del enunciado?
        """
        
        print(report)
        
        with open('test_results.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        if percentage >= 60:
            print("\n✅ APROBADO")
            sys.exit(0)
        else:
            print("\n❌ REPROBADO - Completa el taller según las instrucciones")
            sys.exit(1)

if __name__ == "__main__":
    import os
    
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    
    if not notebook_files:
        print("❌ ERROR: No se encontró ningún archivo .ipynb")
        sys.exit(1)
    
    target = next((f for f in notebook_files if 'taller' in f.lower()), notebook_files[0])
    
    print(f"🔍 Evaluando: {target}")
    print("="*70)
    tester = TallerEstrictoTester(target)
    tester.run_tests()
