# PRODUCTO - OPENJA
**Estado:** Fase de diseño y kickoff

---

## 📋 DOCUMENTOS PRINCIPALES

### 1. **ZONA-CALIDA-OPENJA.md**
Marco filosófico y protocolo de colaboración entre los 5 agentes (JAVI, CLAUDE, CLAUDE CODE, GEMMA, GEMINI).
- Principios no-negociables
- Protocolo de propuesta-debate-decisión
- Reglas de oro para evitar sesgos

**Status:** ✅ RE-LANZADO Y PULIDO

---

### 2. **PLAN-OPENJA.md**
Especificación ejecutable del proyecto.
- Arquitectura alta
- 3 Fases (MVP 0.01, v0.5, v1.0+)
- Tareas divididas por agente (@GEMMA, @GEMINI, @CLAUDE)
- Wall time (minutos/horas, sin tiempos humanos)
- Dependencias y crítica path

**Status:** ✅ CONFIRMADO

---

### 3. **DECISION-LOG.md** (Por crear)
Registro de decisiones importantes.
- Quién decidió, cuándo, por qué
- Alternativas consideradas
- Revisión (si fue correcta o no)

**Status:** 📅 Crear al kickoff

---

## 🚀 KICKOFF

**Próximos pasos:**
1. ✅ Pushear PRODUCTO a GitHub privado
2. ✅ Crear DECISION-LOG.md
3. 🚀 **START MVP: Hora 0**
   - @CLAUDE: C.1, C.2, C.3 (specs)
   - @GEMMA: A.1 (FastAPI)
   - @GEMINI: B.1 (React)

---

## 📂 ESTRUCTURA (FUTURO)

```
PRODUCTO/
├─ ZONA-CALIDA-OPENJA.md (marco filosófico)
├─ PLAN-OPENJA.md (spec ejecutable)
├─ DECISION-LOG.md (historia de decisiones)
├─ docs/
│  ├─ API-SPEC.md (endpoints REST)
│  ├─ DB-SCHEMA.md (SQLite detallado)
│  ├─ BITACORA-TEMPLATE.md (template para agentes)
│  └─ SOUL-TEMPLATE.md (template para identidad agente)
├─ src/ (código, creado post MVP)
└─ tests/ (testing, creado post MVP)
```

---

## 🎯 PRINCIPIOS OPENJA

- **Cada agente = sujeto autónomo con memoria persistente**
- **Gobernanza por APIs, no policía**
- **Sandboxing inviolable**
- **Multi-usuario, multi-agente, colaborativo**
- **Zona Calida = diálogo sin sesgos**

---

## 📞 CONTACTO / ESCALACIÓN

- **Decisiones técnicas:** Zona Calida format
- **Bloqueadores:** Escalá a @JAVI
- **Cambios arquitectónicos:** Debate en ZONA-CALIDA-OPENJA.md
- **Errores/bugs:** Document en DECISION-LOG.md post-mortems

---

**Última actualización:** 12 abril 2026
**Próxima revisión:** Post v0.01
