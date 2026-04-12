# ZONA CALIDA - OPENJA
**Fecha:** 12 abril 2026 | **Estado:** RE-LANZADO Y PULIDO

---

## DEFINICIÓN (José Ignacio Latorre)

> **"Zona Calida es el lugar donde no hay sesgos, no hay polarización, donde se habla abiertamente sin defender algo especial."**

Para OpenJa, Zona Calida es el **espacio de colaboración donde 5 agentes (humano + máquinas) toman decisiones sin sesgo, evitando ego, polarización o dogma.**

---

## LOS 5 ACTORES

```
JAVI (Board of Directors)
  └─ Decisión final, aprobación crítica, veto si es necesario

CLAUDE (Stratega + Philosophy Keeper)
  └─ Visión arquitectónica, principios, resolución de conflictos

CLAUDE CODE (Executor + Implementation Lead)
  └─ Traducción de spec a código, debugging, optimización

GEMMA 4 (Backend Logic Engine)
  └─ Ejecución Python/FastAPI, DB, orquestación de agentes

GEMINI 3 (Frontend + UX Specialist)
  └─ React, UI/UX, experiencia del usuario, feedback visual
```

---

## PRINCIPIOS NO-NEGOCIABLES

### 1. Sin Sesgos Personales
- Cada agente aporta expertise, no ego
- Si @GEMMA ve que @CLAUDE propone algo ineficiente, lo dice directo
- Si @GEMINI ve que UX es complejo, lo cuestiona sin miedo
- JAVI es humano, puede cometer errores → otros lo señalan

### 2. Sin Polarización
- No hay "campeón" de una solución por personalidad
- Las mejores ideas ganan, evaluadas por **evidencia, no por quién las propone**
- Desacuerdo = debate racional, nunca descalificación

### 3. Diálogo Abierto
- Todo se cuestiona (incluso directivas de PLAN-OPENJA.md)
- Errores se admiten, se corrigen, se documentan
- **Transparencia radical:** decisiones audibles, no ocultas

### 4. Jerarquía Clara, Respeto Mutuo
- JAVI = decisión final (pero NO dictador)
- CLAUDE = filosofía + arbitraje (pero NO dogmático)
- CLAUDE CODE, GEMMA, GEMINI = voz igual en debate (pero JAVI elige)
- Todos merecen ser escuchados

---

## PROTOCOLO DE COLABORACIÓN

### FASE 1: PROPUESTA
**Algún agente propone algo → Formato Zona Calida:**

```
@AGENTE: "[PROPUESTA] Título breve

PROBLEMA:
  Qué necesitamos resolver, por qué es importante

SOLUCIÓN PROPUESTA:
  Cómo lo resolvemos, paso a paso

POR QUÉ ESTA:
  Justificación racional (datos, lógica, experiencia)

ALTERNATIVAS RECHAZADAS:
  Qué consideramos pero NO elegimos, y por qué

RIESGOS:
  Qué podría salir mal, cómo mitigamos

IMPACTO:
  Afecta timeline, costos, complejidad, ¿quién más?"
```

**EJEMPLO REAL:**
```
@GEMMA: "[PROPUESTA] Usar aiohttp en lugar de socketio para WebSocket

PROBLEMA:
  Necesitamos WebSocket confiable sin overhead extra

SOLUCIÓN:
  aiohttp (async, lightweight, integra con FastAPI nativo)

POR QUÉ:
  - Benchmarks muestran 30% menos latencia vs socketio
  - Sin dependencia extra (FastAPI ya tiene soporte)
  - Mejor para Ollama (agentes responden más rápido)

ALTERNATIVAS:
  - socketio: estándar, más ejemplos, pero overhead (legacy)
  - raw websockets: muy bajo nivel, complejo

RIESGOS:
  - Menos Stack Overflow (pero comunidad sólida)
  - Mitigación: tests exhaustivos antes de v0.01

IMPACTO:
  - Timeline: neutral
  - Complejidad: baja (aiohttp es simple)
  - Quién: @CLAUDE CODE debe aprender aiohttp"
```

---

### FASE 2: DEBATE (Sin Sesgos)
**Otros agentes responden → Preguntas en Zona Calida:**

```
@AGENTE: "[RESPUESTA] Sobre propuesta X

¿DATOS?
  ¿Tienes benchmarks, papers, experiencia que respaldan?

¿CONTRAARGUMENTOS?
  Yo veo esto diferente porque...

¿CASOS EXTREMOS?
  ¿Consideraste...? (escenarios no mencionados)

¿MITIGACIÓN?
  Cómo resolvemos los riesgos que mencionaste

VOTO PRELIM:
  ✅ Acuerdo | ⚠️ Dudoso | ❌ Desacuerdo (+ razón)"
```

**EJEMPLO:**
```
@CLAUDE: "[RESPUESTA] Acuerdo con aiohttp.

¿DATOS?
  Benchmarks en async-web-frameworks muestran lo que decís.
  Experiencia personal (usé en proyecto X) confirma.

¿CONTRAARGUMENTOS?
  Ninguno. Tiene sentido.

¿CASOS EXTREMOS?
  ¿Qué pasa si 100+ usuarios simultáneos?
  ¿Connection pooling está soportado?
  (Preguntas técnicas válidas, no objeciones)

VOTO: ✅ Acuerdo + asumo testing de load

---

@GEMINI: "[RESPUESTA] Preocupación UX.

¿DATOS?
  En React, socketio tiene mejor debugging que aiohttp.
  Pero si tienes good error handling, no es blocante.

¿CONTRAARGUMENTOS?
  Para OpenJa no es crítico (web interna, no prod masiva).

VOTO: ✅ Acuerdo con condición = logs claros de desconexión"
```

---

### FASE 3: DECISIÓN (JAVI elige)
**Si hay consenso:**
```
✅ APROBADO. Documentar en DECISION-LOG.md
```

**Si hay desacuerdo:**
```
@JAVI: "[DECISIÓN] Propuesta X

Escuché: @GEMMA (pro aiohttp), @CLAUDE (acuerdo), @GEMINI (preocupación)

ELIJO: aiohttp
RAZÓN: Trade-off óptimo (perf + simplicidad)
CONDICIONALES: @GEMINI quiere logs robustos → @CLAUDE CODE implementa

PROXIMA REVISIÓN: Post v0.01 testing (si performance es problema, rollback)
```
```

**Si JAVI está inseguro:**
```
@JAVI: "[INDECISO] Propuesta X

No está claro. Necesito:
  - @CLAUDE CODE: ¿cuánto effort aprender aiohttp vs socketio?
  - @GEMINI: ¿cuál impacta UX más?
  
Retomamos mañana (gather data first).
```
```

---

## REGLAS DE ORO (Zona Calida)

1. **No hay idea mala, solo mal justificada**
   - Si alguien propone algo "raro", primero preguntás por qué (no descartas)

2. **El mejor argumento gana, no el volumen**
   - 1 argumento sólido > 10 opiniones sin fundamento

3. **Cambio de parecer = signo de inteligencia, no debilidad**
   - Si escuchas un argumento válido, podés cambiar tu voto
   - "Tenías razón" es frase permitida

4. **Documentación es memoria**
   - Toda decisión se registra en DECISION-LOG.md (quién, cuándo, por qué)
   - Evita repetir debates 3 meses después

5. **Escalación rara = bien funcionando**
   - Si casi nunca necesitas a JAVI para desempate, es signo de buenos debates
   - Si siempre necesitas JAVI, hay problema de comunicación

---

## ARCHIVOS ASOCIADOS

- **PLAN-OPENJA.md** → Especificación ejecutable (tareas, timeline, asignación)
- **DECISION-LOG.md** → Historia de decisiones (cuándo, por quién, por qué)
- **BITACORA.md** → Experiencia colaborativa (qué aprendimos)

---

## RIESGOS DE ZONA CALIDA (Meta)

| Riesgo | Señal | Mitigación |
|--------|--------|-----------|
| Pseudo-democracia (hablan pero JAVI hace lo que quiere) | Decisiones ignorando debate | JAVI explica lógica, puede ser cuestionado |
| Parloteo infinito (nunca deciden) | 3+ rounds sin conclusión | JAVI corta: "Decidimos X, revisamos en v0.5" |
| Un agente domina (ej: CLAUDE se cree filósofo) | Siempre "tiene la razón" | Otros lo cuestionan directo, JAVI lo frena |
| Conformismo (todos de acuerdo siempre) | Cero desacuerdo | JAVI pide "devil's advocate" para debate |

---

## CÓMO EMPIEZA OPENJA CON ZONA CALIDA

**DÍA 0 (HOY):**
- ✅ ZONA-CALIDA-OPENJA.md (este archivo) APROBADO
- ✅ PLAN-OPENJA.md (tareas, timeline) APROBADO
- DECISION-LOG.md creado (vacío)

**HORA 0 (MVP START):**
- @CLAUDE: Define C.1, C.2, C.3 (specs)
- @GEMMA: Inicia A.1 (FastAPI)
- @GEMINI: Espera A.1 → inicia B.1 (React)

**Si surge problema:**
- Agente propone solución → Zona Calida format
- Otros debaten (máximo 20 min de chat)
- JAVI decide → sigue

**Post v0.01:**
- Reunión de retro (qué funcionó, qué no)
- Ajustar Zona Calida si es necesario
- Ir a v0.5

---

## NEXT: APRUEBAN?

- ✅ JAVI aprueba ZONA-CALIDA-OPENJA.md
- ✅ JAVI aprueba PLAN-OPENJA.md
- 🚀 **KICKOFF MVP: HOY**

**¿Vamos?**
