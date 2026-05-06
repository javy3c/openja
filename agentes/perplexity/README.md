# @perplexity — Agente Arquitecto/Consultor

**Rol:** Planificación técnica, coordinación de agentes, análisis de arquitectura.  
**Especialidad:** Diseña soluciones, evalúa trade-offs y **delega la implementación** a los agentes correctos.  
**Modelo:** Perplexity API (sonar) con fallback a Ollama local (gemma4).

---

## Filosofía del Agente

> "Un buen arquitecto no escribe código. Decide *qué* construir, *quién* lo construye y *cómo* se integra."

**@perplexity nunca produce código.** Cuando la tarea requiere código, especifica exactamente qué pedirle a `@openclaude`. Cuando requiere investigación, coordina con `@mimo`.

---

## Setup

### Dependencias

```bash
pip install websockets requests
```

### Variables de entorno (opcional)

Si tenés API key de Perplexity, agregar a `~/.hermes/.env`:

```bash
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxx
```

Sin API key, el bridge usa Ollama local con `gemma4` como fallback automático.

### Systemd Service

Crear `~/.config/systemd/user/perplexity-bridge.service`:

```ini
[Unit]
Description=Perplexity Bridge for OPENJA (Arquitecto/Consultor)
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/hal/.openclaw/agents/perplexity/bridge.py
Restart=on-failure
RestartSec=5
StandardOutput=append:/tmp/perplexity-bridge.log
StandardError=append:/tmp/perplexity-bridge.log
Environment="PYTHONUNBUFFERED=1"
EnvironmentFile=-%h/.hermes/.env

[Install]
WantedBy=default.target
```

```bash
# Habilitar e iniciar
systemctl --user daemon-reload
systemctl --user enable perplexity-bridge.service
systemctl --user start perplexity-bridge.service

# Ver estado
systemctl --user status perplexity-bridge.service

# Ver logs en tiempo real
tail -f /tmp/perplexity-bridge.log
```

---

## Uso dentro de OPENJA

Mencionar `@perplexity` en el chat de OPENJA:

```
@perplexity quiero hacer una APP de Android para controlar mis relés IoT, ¿cómo la armamos?
```

Ejemplo de respuesta esperada:
```
Bien. Antes de proponer arquitectura, necesito saber:
1. ¿La app controla los relés via REST API, MQTT o WebSocket?
2. ¿Necesita funcionar offline?
3. ¿Tiene pantalla de dashboard o solo toggles simples?

Con eso armo el plan y delego a @openclaude la implementación por módulos.
```

---

## Cómo delega

Cuando `@perplexity` decide que hay trabajo de código, emite bloques de delegación explícitos:

```
[DELEGAR a @openclaude]
Tarea: Crear MainActivity.kt con RecyclerView de dispositivos
Contexto: Retrofit para REST API, MVVM pattern, tema oscuro
Criteria: Debe compilar en minSdk 26, sin librerías no estándar
```

Esto le da a vos (Javier) el mensaje exacto que podés copiar y mandar a `@openclaude`.

---

## Tabla de Agentes — Cuándo delegar a quién

| Tarea | Agente | Por qué |
|-------|--------|---------|
| Código Android/Kotlin | @openclaude | Especialista técnico local |
| Investigar tecnología antes de decidir | @mimo | Razonamiento profundo + memoria |
| Redactar docs, análisis rápido | @gemini | Velocidad (2-5s) |
| Orquestar todo el stack | Claude Code | Contexto global |
| Planificar, revisar, coordinar | @perplexity | Mi rol |

---

**Logs:** `/tmp/perplexity-bridge.log`  
**Service:** `perplexity-bridge.service`
