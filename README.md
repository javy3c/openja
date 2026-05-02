# OPENJA — Sistema de Agentes Autónomos Colaborativos

**Producto:** Personal AI Presence con gobernanza API, memoria persistente, y aislamiento de seguridad.

**Estado:** MVP en desarrollo (fase kickoff → 0.01)

---

## 📦 Estructura del Repositorio

```
openja/
├── ZONA-CALIDA-OPENJA.md          Filosofía + protocolo de colaboración
├── PLAN-OPENJA.md                 Especificación técnica y roadmap
├── DECISION-LOG.md                (próximas decisiones importantes)
│
├── arquitectura/                   Documentación técnica de sistemas
│   ├── OPENJA_LOCAL_AGENTS_ARCHITECTURE.md   (MiMo, OpenClaude, Gateway)
│   ├── OPENJA_GEMINI_ARCHITECTURE.md        (Agente Gemini remoto)
│   └── README.md                   Índice de arquitectura
│
├── agentes/                        Implementación de agentes
│   ├── mimo/                       Razonamiento local + Memory+RAG
│   ├── openclaude/                 Código técnico local
│   ├── gemini/                     Análisis remoto (Google Cloud)
│   └── README.md                   Índice de agentes
│
├── operacional/                    Procedimientos y monitoreo
│   ├── health-check.sh             Script de verificación
│   ├── recovery-procedures.md      Solución de problemas
│   └── README.md                   Índice operacional
│
└── desarrollo/                     Planes técnicos futuros
    ├── api-spec.md                 Especificación de APIs
    ├── database-schema.md          Diseño de persistencia
    └── README.md                   Índice de desarrollo
```

---

## 🎯 Principios Clave

1. **Cada agente = sujeto autónomo** con identidad, memoria, y responsabilidades
2. **Gobernanza por API** — no supervisión centralizada
3. **Aislamiento de seguridad** — sandboxing inviolable
4. **Privacy by design** — datos del usuario bajo su control
5. **Colaboración multi-nivel** — agentes pueden comunicarse entre sí

---

## 🚀 Agentes del Sistema

| Agente | Modelo | Especialidad | Infraestructura |
|--------|--------|--------------|-----------------|
| **@mimo** | mimo-7b (4.7GB) | Razonamiento profundo, investigación | Ollama + SQLite FTS5 |
| **@openclaude** | gemma4 (9.6GB) | Código, arquitectura técnica | Ollama |
| **@gemini** | Gemini 2.5 Flash (API) | Análisis general, escritura rápida | Google Cloud |
| **Claude Code** | claude-haiku-4.5 | Contexto remoto, orquestación | Anthropic API |

---

## 📖 Documentación Principal

- **[ZONA-CALIDA-OPENJA.md](ZONA-CALIDA-OPENJA.md)** — Marco filosófico y protocolo de Zona Cálida
- **[PLAN-OPENJA.md](PLAN-OPENJA.md)** — Especificación ejecutable con 3 fases
- **[arquitectura/](arquitectura/)** — Documentación técnica detallada
  - [OPENJA_LOCAL_AGENTS_ARCHITECTURE.md](arquitectura/OPENJA_LOCAL_AGENTS_ARCHITECTURE.md) ⭐ **Recomendado: empezar aquí**
  - [OPENJA_GEMINI_ARCHITECTURE.md](arquitectura/OPENJA_GEMINI_ARCHITECTURE.md)

---

## ⚙️ Cómo Usar Este Repositorio

### Para Entender el Sistema
1. Lee [ZONA-CALIDA-OPENJA.md](ZONA-CALIDA-OPENJA.md) (filosofía)
2. Lee [PLAN-OPENJA.md](PLAN-OPENJA.md) (roadmap)
3. Consulta [arquitectura/OPENJA_LOCAL_AGENTS_ARCHITECTURE.md](arquitectura/OPENJA_LOCAL_AGENTS_ARCHITECTURE.md) (detalles técnicos)

### Para Desarrollar
1. Revisa [desarrollo/](desarrollo/) para specs de APIs
2. Consulta [agentes/](agentes/) para implementación
3. Usa [operacional/](operacional/) para health checks

### Para Operar
1. Ver [operacional/health-check.sh](operacional/health-check.sh)
2. Usar [operacional/recovery-procedures.md](operacional/recovery-procedures.md) si algo falla
3. Revisar logs en `/tmp/*-bridge.log`

---

## 📋 Estado Actual

- ✅ Documentación de arquitectura completa
- ✅ Agentes locales operacionales (MiMo + OpenClaude)
- ✅ Gateway Zona Cálida funcionando
- ✅ Memory + RAG system implementado
- ⏳ API spec detallada (en desarrollo)
- ⏳ Database schema (próximo)
- ⏳ Deployment automatizado (MVP 0.5)

---

## 🔄 Cómo Contribuir

1. Consulta [DECISION-LOG.md](DECISION-LOG.md) para decisiones anteriores
2. Propón cambios en issues o PRs
3. Mantén documentación al día
4. Sigue convenciones de ZONA-CALIDA

---

## 📚 Referencias

- **Repo de documentación general:** github.com/javy3c/openclaw-docs
- **HAL Vision:** openclaw-docs/hal-eternal/vision.md
- **Bitácoras:** openclaw-docs/bitacoras/

---

**Maintained by:** Javier Guerrero, Claude (Anthropic)  
**Last Updated:** 2026-05-02  
**Repository:** github.com/javy3c/openja
