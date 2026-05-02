# Arquitectura de OPENJA

Documentación técnica detallada del sistema de agentes y Gateway.

## Documentos

- **OPENJA_LOCAL_AGENTS_ARCHITECTURE.md** — Agentes locales (MiMo-7B, OpenClaude), Memory+RAG, sistema de mensajes, failure modes
- **OPENJA_GEMINI_ARCHITECTURE.md** — Arquitectura del agente Gemini (API remota)

## Componentes Cubiertos

- Zona Cálida Gateway (WebSocket bus, HTTP dashboard)
- MiMo-7B (razonamiento + memory)
- OpenClaude (código técnico)
- Gemini (análisis remoto)
- Claude Code (contexto remoto)

## Performance & Operación

- Benchmarks reales de latencia
- VRAM management (coexistencia multi-modelo)
- Recovery procedures completas
- Monitoring y health checks
