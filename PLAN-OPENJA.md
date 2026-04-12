# OPENJA - PLAN MAESTRO
**Fecha:** 12 abril 2026 | **Estado:** DISEÑO FORMAL

---

## VISIÓN
OpenJa = Orquestador de agentes multi-tier, multi-user, con memory persistente, UI visual, gobernanza por APIs, sandboxing inviolable.

**Principios:**
- Cada agente = sujeto autónomo con experiencia persistente
- Gobernanza por APIs, no policía
- Sandboxing = arquitectura no negociable
- Agentes T0+T2 libres, T1 presupuestado
- Linux-first (Ubuntu 24.04), web-based

---

## ARQUITECTURA ALTA

```
OPENJA BACKEND (Python Flask/FastAPI)
├── Orquestador central (logic, dispatch)
├── Agent Manager (systemd + Ollama)
├── Room Manager (state, chat, tasks)
├── Memory Vault (SOUL.md, BITACORA.md)
├── Secrets Vault (.env MVP → SQLite v0.5)
├── API Gateway (REST + WebSocket)
└── DB (SQLite: tasks, projects, users, audit)

OPENJA FRONTEND (React)
├── Dashboard (topología visual)
├── Rooms (chat + visualización)
├── Tablero de tareas (Kanban)
├── Agent pool (drag & drop)
├── Insignias/scoring
└── Auditoría/logs

AGENTES (systemd services)
├── T0: Robots (bash/python scripts)
├── T1: Cerebritos (Haiku via API)
├── T2: Cerebro pesado (Gemma 4 via Ollama)
└── T3: Consultores (vos, Gemini, Claude - manual)

INFRA
├── Ubuntu 24.04 (kernel base)
├── Ollama (Gemma 4 en RTX 3060)
├── systemd (process manager)
├── SQLite (state)
├── Tailscale (optional: acceso remoto)
└── WhatsApp/Discord (notificaciones)
```

---

## FASES

### FASE 1: MVP (Beta 0.01) - EJECUCIÓN PARALELA
**Objetivo:** Proof of Concept funcional
- 1 room
- 2 agentes (Operario/Gemma 4 local)
- Chat básico con @mentions
- Tablero de tareas (To-do → In-progress → Done)
- Memory persistente (BITACORA.md)

**ASIGNACIÓN DE TAREAS:**

---

### BLOQUE A: BACKEND (@GEMMA - Python/FastAPI)
**Duración estimada:** ~3-4 horas paralelas

```
A.1 FastAPI scaffold + SQLite schema
  @GEMMA - Python
  - FastAPI app init
  - SQLite DB (schema: users, rooms, agents, tasks, chat, audit_log)
  - Pydantic models
  - CRUD básico (tasks, rooms)
  - Duración: 45 min
  - Depende de: nada
  - Bloquea: A.2, A.3, A.4

A.2 WebSocket setup
  @GEMMA - Python
  - python-socketio + aiohttp
  - Broadcast a clientes
  - Message routing
  - Duración: 30 min
  - Depende de: A.1
  - Bloquea: A.4, B.3

A.3 Agent Manager (Ollama wrapper)
  @GEMMA - Python
  - REST client para Ollama (localhost:11434)
  - Healthcheck (5s polling)
  - Message serialization
  - systemd status reader
  - Duración: 45 min
  - Depende de: A.1
  - Bloquea: A.5

A.4 Chat @mentions parser + routing
  @GEMMA - Python
  - Regex parser (@agentname)
  - Route a agente específico
  - BITACORA logging (append-only)
  - Duración: 30 min
  - Depende de: A.1, A.2
  - Bloquea: A.5

A.5 Room + Task logic
  @GEMMA - Python
  - Create room (POST /rooms)
  - Add agent to room (POST /rooms/{id}/agents)
  - Task CRUD (POST/GET/PUT /tasks)
  - Task state machine (To-do → In-progress → Done)
  - Duración: 45 min
  - Depende de: A.1, A.3, A.4
  - Bloquea: Testing

A.6 Auth MVP (hardcoded)
  @GEMMA - Python
  - Simple token (user:password)
  - Middleware check
  - Duración: 15 min
  - Depende de: A.1
  - Bloquea: nada crítico MVP
```

**EJECUCIÓN PARALELA POSIBLE:**
- A.1 (45 min) → luego A.2, A.3 paralelo (30+45 min) → A.4, A.5 paralelo (30+45 min)
- **TOTAL A.x:** ~2.5 horas secuencial, ~1.5-2 horas pared (si paralelo)

---

### BLOQUE B: FRONTEND (@GEMINI - React)
**Duración estimada:** ~3-4 horas paralelas

```
B.1 React app scaffold + WebSocket client
  @GEMINI - JavaScript/React
  - Create React app (Vite si es rápido)
  - socket.io-client setup
  - State management (Zustand/Redux minimal)
  - Duración: 30 min
  - Depende de: A.2 (WebSocket server vivo)
  - Bloquea: B.2, B.3, B.4

B.2 Chat component
  @GEMINI - React
  - Message list (scrollable)
  - Input field
  - @mention autocomplete
  - WebSocket listener (real-time messages)
  - Duración: 45 min
  - Depende de: B.1, A.4
  - Bloquea: Integration testing

B.3 Kanban Tablero (tasks)
  @GEMINI - React
  - 3 columns (To-do, In-progress, Done)
  - Drag & drop (react-beautiful-dnd)
  - Task cards (title, assignee, status)
  - Task state update (PATCH /tasks)
  - Duración: 45 min
  - Depende de: B.1, A.5
  - Bloquea: Integration testing

B.4 Agent pool visual
  @GEMINI - React
  - List de agentes (nombre, status, score)
  - Drag & drop agentes a room (v0.5, MVP = static)
  - Assignee dropdown (en tasks)
  - Duración: 30 min
  - Depende de: B.1
  - Bloquea: Integration testing

B.5 Styling (Tailwind)
  @GEMINI - CSS
  - Basic layout (sidebar, main area, chat area)
  - Responsive (desktop MVP, mobile v1.0)
  - Dark mode (optional)
  - Duración: 30 min
  - Depende de: B.2, B.3, B.4
  - Bloquea: Polish
```

**EJECUCIÓN PARALELA POSIBLE:**
- B.1 (30 min) → B.2, B.3, B.4 paralelo (~1.5 horas) → B.5 (30 min)
- **TOTAL B.x:** ~2.5 horas secuencial, ~1.5-2 horas pared (si paralelo)

---

### BLOQUE C: ARQUITECTURA & INTEGRACIÓN (@CLAUDE - Vos)
**Duración estimada:** ~2-3 horas secuencial

```
C.1 Spec API endpoints (REST)
  @CLAUDE - Diseño
  - POST /rooms (crear room)
  - POST /rooms/{id}/agents (agregar agente)
  - POST /tasks (crear task)
  - PATCH /tasks/{id} (actualizar estado)
  - GET /tasks (listar tasks del room)
  - GET /agents (status de agentes)
  - POST /chat (enviar mensaje)
  - Duración: 30 min
  - Depende de: visión arquitectónica
  - Bloquea: A.x, B.x validación

C.2 BITACORA.md schema
  @CLAUDE - Diseño
  - Estructura de memoria por agente
  - Formato de registro (JSON/YAML)
  - Persistencia (archivo local ~/openja/bitacoras/{agent_id}.md)
  - Duración: 15 min
  - Depende de: A.4 (chat logic)
  - Bloquea: A.4 finalización

C.3 SQLite schema (detallado)
  @CLAUDE - Diseño
  - Tablas: users, rooms, agents, tasks, messages, audit_log
  - Índices y relaciones
  - Constraints
  - Duración: 20 min
  - Depende de: visión de features
  - Bloquea: A.1 validación

C.4 Integration testing plan
  @CLAUDE - QA
  - Flow: crear task → asignar agente → @mention → agente responde → tarea done
  - Casos edge (timeout, agente offline)
  - Duración: 30 min
  - Depende de: A.x + B.x completo
  - Bloquea: C.5

C.5 Go/no-go decisión (MVP listo?)
  @CLAUDE - Decisión
  - Review de A.x, B.x, tests
  - ¿Qué falta crítico para 0.01?
  - Duración: 15 min
  - Depende de: C.4 testing
  - Bloquea: FASE 2
```

**EJECUCIÓN:** Paralelo con A.x y B.x (no bloquea), secuencial para validación final

---

### CRÍTICO: ORDENAMIENTO DE EJECUCIÓN

```
TIEMPO 0: START
├─ A.1 (FastAPI + SQLite) ................ 45 min
│  ├─ A.2 (WebSocket) ................... 30 min
│  ├─ A.3 (Ollama wrapper) .............. 45 min
│  └─ A.6 (Auth) ....................... 15 min
│
├─ PARALELO: B.1 (React) ............... 30 min
│  ├─ B.2 (Chat) ....................... 45 min
│  ├─ B.3 (Kanban) .................... 45 min
│  └─ B.4 (Agent pool) ................ 30 min
│  └─ B.5 (Styling) ................... 30 min
│
├─ PARALELO: C.1 (Spec API) ........... 30 min
├─ PARALELO: C.2 (BITACORA schema) ... 15 min
├─ PARALELO: C.3 (DB schema) ......... 20 min
│
└─ A.4 (Chat @mentions) [depende A.1, A.2] ................. 30 min
└─ A.5 (Room + Task logic) [depende A.1, A.3, A.4] ........ 45 min
└─ C.4 (Integration testing) [depende A.x + B.x] ......... 30 min
└─ C.5 (Go/no-go) [depende C.4] .......................... 15 min

PARED CRÍTICA (si Gemma + Gemini paralelo):
├─ Backend critical path: A.1 (45) → A.2+A.3 (45) → A.4+A.5 (75) = ~2.5 hrs
├─ Frontend critical path: B.1 (30) → B.2+B.3+B.4 (120) → B.5 (30) = ~2 hrs
├─ Arquitectura: ~1 hr (paralelo)
└─ TOTAL WALL TIME: ~2.5 hrs (Gemma + Gemini paralelo) + testing/integration
```

**EN RESUMEN:**
- @GEMMA Backend: ~2.5 hrs pared (tareas parallelizadas)
- @GEMINI Frontend: ~2 hrs pared (tareas parallelizadas)
- @CLAUDE: ~1 hr total (paralelo con los otros)
- **TOTAL WALL TIME MVP:** ~2.5-3 horas (si todo paralelo)

---

### FASE 2: Multi-agente (Beta 0.5) - EJECUCIÓN PARALELA
**Objetivo:** Interacción agente-a-agente, scorings básicos, multi-user

**ASIGNACIÓN DE TAREAS:**

---

### BLOQUE D: BACKEND EXTENSIÓN (@GEMMA - Python)
**Duración estimada:** ~3-4 horas paralelas

```
D.1 T1 Integration (Haiku via Anthropic API)
  @GEMMA - Python
  - Anthropic Python SDK setup
  - Presupuesto per-agente (tracking en DB)
  - Cost calculator (tokens → USD)
  - Rate limiting (presupuesto diario)
  - Duración: 60 min
  - Depende de: A.1 (DB)
  - Bloquea: D.5

D.2 Message Queue (async tasks)
  @GEMMA - Python
  - SimpleQueue o Redis para queue
  - Task dispatcher (pick task → assign agent)
  - Timeout handler (30s default)
  - Duración: 45 min
  - Depende de: A.1
  - Bloquea: D.3, D.4

D.3 Agent autonomy (T0/T2 inician)
  @GEMMA - Python
  - Agente puede @mention otro sin user
  - Scoring para iniciativas (+0.5 point per init)
  - Logging (quién pidió a quién)
  - Duración: 30 min
  - Depende de: A.4, D.2
  - Bloquea: D.5

D.4 Scoring & Insignias system
  @GEMMA - Python
  - Task completion → +1 score
  - Task failure → -0.5 score
  - Counter (cada 10 done tasks → insignia)
  - SOUL.md updater (append badge)
  - Duración: 45 min
  - Depende de: A.1, A.5
  - Bloquea: D.5

D.5 Multi-user sandbox
  @GEMMA - Python
  - User auth mejorada (JWT tokens)
  - Per-user workspace (~/openja/users/{user_id})
  - Sandbox isolation (agentes solo acceden recursos del user)
  - Permisos básicos (owner, editor, viewer)
  - Duración: 60 min
  - Depende de: A.6, D.1, D.2
  - Bloquea: Testing

D.6 SQLite encrypted secrets vault
  @GEMMA - Python
  - Migrate de .env → secrets.db
  - AES-256 encryption (cryptography lib)
  - Per-agent credentials (Google Sheets, Tasmota, etc.)
  - Secret rotation helpers
  - Duración: 45 min
  - Depende de: A.1
  - Bloquea: D.5 testing

D.7 Audit trail completa
  @GEMMA - Python
  - INSERT audit_log en cada acción (task created, scored, etc.)
  - Timeline API (GET /audit?user_id=X&days=7)
  - Immutable logs (append-only, nunca delete)
  - Duración: 30 min
  - Depende de: A.1
  - Bloquea: B.x UI
```

**EJECUCIÓN PARALELA:**
- D.1 (60) + D.2 (45) + D.4 (45) paralelo → D.3 (30) + D.5 (60) → D.6 (45) + D.7 (30)
- **TOTAL D.x:** ~3 horas pared

---

### BLOQUE E: FRONTEND EXTENSIÓN (@GEMINI - React)
**Duración estimada:** ~2-3 horas paralelas

```
E.1 Multi-user UI (auth flow)
  @GEMINI - React
  - Login/logout component
  - User profile widget
  - Switch user (si es admin)
  - JWT token storage (localStorage)
  - Duración: 30 min
  - Depende de: D.5 backend
  - Bloquea: E.2

E.2 Scoring & Badge display
  @GEMINI - React
  - Agent card muestra score (0-100)
  - Badge list (insignias ganadas)
  - Notification cuando score +10 (popup)
  - Duración: 30 min
  - Depende de: E.1, D.4
  - Bloquea: Testing

E.3 Audit timeline UI
  @GEMINI - React
  - Timeline view (quién hizo qué, cuándo)
  - Filter por user/agent/action
  - Expandable events (mostrar detalles)
  - Duración: 45 min
  - Depende de: D.7
  - Bloquea: Polish

E.4 Cost dashboard (T1 budget)
  @GEMINI - React
  - Bar chart (USD usage per agent)
  - Remaining budget (visual)
  - Warning si approaching limit
  - Duración: 30 min
  - Depende de: D.1
  - Bloquea: Polish
```

**EJECUCIÓN PARALELA:**
- E.1 (30) → E.2 (30) + E.3 (45) + E.4 (30) paralelo
- **TOTAL E.x:** ~1.5 horas pared

---

### BLOQUE F: ARQUITECTURA VALIDACIÓN (@CLAUDE - Vos)
**Duración estimada:** ~2 horas

```
F.1 Spec de autonomía agente
  @CLAUDE - Diseño
  - Cuándo agente puede iniciar
  - Límites (no loop infinito)
  - Escalación rules
  - Duración: 20 min
  - Depende de: D.3
  - Bloquea: Testing

F.2 Scoring formula
  @CLAUDE - Diseño
  - Task done = +1
  - Task fail = -0.5
  - Autonomy init bonus = +0.5
  - Cap max = 100
  - Duración: 15 min
  - Depende de: D.4
  - Bloquea: D.4 validation

F.3 Sandbox security review
  @CLAUDE - Security
  - ¿Agente X puede escapar su sandbox?
  - ¿API keys leakean entre users?
  - Penetration testing plan
  - Duración: 30 min
  - Depende de: D.5, D.6
  - Bloquea: Production release

F.4 Integration test (multi-user)
  @CLAUDE - QA
  - User A + Agente X
  - User B + Agente Y
  - ¿Se contaminan o aislados?
  - Cost tracking por user
  - Duración: 30 min
  - Depende de: D.x + E.x
  - Bloquea: FASE 3

F.5 Go/no-go v0.5
  @CLAUDE - Decisión
  - ¿Multi-user ready?
  - ¿Agentes se comunican sin errores?
  - ¿Costos trackeable?
  - Duración: 15 min
  - Depende de: F.4
  - Bloquea: FASE 3
```

---

### PARED CRÍTICA FASE 2

```
PARALELO (Wall time):
├─ Backend: D.1+D.2+D.4 (150 min) → D.3+D.5 (90 min) → D.6+D.7 (75 min) = ~3.5-4 hrs
├─ Frontend: E.1 (30) → E.2+E.3+E.4 (105) = ~2.25 hrs
├─ Arquitectura: ~1.5 hrs (paralelo)
└─ TOTAL WALL TIME: ~3.5-4 horas (Gemma + Gemini paralelo)
```

**EN RESUMEN:**
- @GEMMA Backend: ~3.5 hrs pared
- @GEMINI Frontend: ~2.25 hrs pared
- @CLAUDE: ~1.5 hrs (paralelo)
- **TOTAL WALL TIME v0.5:** ~3.5-4 horas

---

### FASE 3: Refinamientos (v1.0+) - EJECUCIÓN VARIABLE
**Objetivo:** Producción-ready, topología visual, God Mode

**ASIGNACIÓN (continúa patrón A/B/C):**

```
G.1 Topología visual (cables + rooms gráficas)
  @GEMINI - React
  - React Flow library (nodes + edges)
  - Room = node, cables = edges
  - Drag & drop agentes between rooms (v1.0)
  - Real-time updates (WebSocket)
  - Duración: 90-120 min

G.2 God Mode (intervención en tiempo real)
  @CLAUDE - Logic + @GEMINI - UI
  - Pause/resume agente
  - Override task assignment
  - Emergency shutdown agent
  - Duración: 60 min

G.3 Webhooks/Integraciones
  @GEMMA - Python
  - Email → create task
  - Slack → room notification
  - GitHub → task assignment
  - Duración: 90 min

G.4 Health Dashboard
  @GEMINI - React
  - Real-time metrics (uptime, latencia, temp GPU)
  - Alert system (si T2 approaching limit)
  - Duración: 60 min

G.5 Portabilidad (Mac/Windows)
  @GEMMA - Python
  - Abstracción process manager (systemd/launchd/Task Scheduler)
  - PM2 integration
  - Duración: variable (post MVP)
```

---

## STACK TÉCNICO (CONFIRMADO)

**Backend:**
- Framework: FastAPI (async, rápido)
- WebSocket: python-socketio
- Agent control: systemd + subprocess
- DB: SQLite (MVP → PostgreSQL si escalás)
- Encryption: cryptography (AES-256 para secrets)

**Frontend:**
- React 18+ (Vite)
- WebSocket client: socket.io-client
- UI: Tailwind CSS
- State: Zustand (lightweight)
- Graphs: React Flow (G.1), Recharts (metrics)

**Agentes:**
- T0: bash/python3 scripts
- T1: Anthropic API client
- T2: Ollama + Python client
- T3: Manual (Discord/Chat)

**Infra:**
- systemd (process manager)
- Ollama (LLM local, RTX 3060)
- SQLite (embedded, no server needed)

---

## CRONOGRAMA REVISADO (sin "semanas")

| Fase | Wall time | Paralelo | Estado | Inicio |
|------|-----------|----------|--------|--------|
| **MVP 0.01** | ~2.5-3 hrs | Gemma + Gemini + Claude | Planeada | Hoy |
| **Multi 0.5** | ~3.5-4 hrs | Gemma + Gemini + Claude | Planeada | Post MVP |
| **v1.0+** | Variable | Features + polish | Planeada | Post 0.5 |

---

## ASIGNACIÓN FINAL (RESUMIDA)

```
@GEMMA (Backend Python):
├─ FastAPI + SQLite (A.1)
├─ WebSocket (A.2)
├─ Ollama wrapper (A.3)
├─ Chat parser (A.4)
├─ Room/Task logic (A.5)
├─ Haiku integration (D.1)
├─ Message queue (D.2)
├─ Scoring (D.4)
├─ Multi-user sandbox (D.5)
├─ Secrets vault (D.6)
├─ Audit logs (D.7)
└─ Webhooks (G.3)

@GEMINI (Frontend React):
├─ React scaffold (B.1)
├─ Chat component (B.2)
├─ Kanban tablero (B.3)
├─ Agent pool (B.4)
├─ Styling (B.5)
├─ User auth UI (E.1)
├─ Scoring display (E.2)
├─ Audit timeline (E.3)
├─ Cost dashboard (E.4)
├─ Topología visual (G.1)
└─ Health dashboard (G.4)

@CLAUDE (Architecture + QA + Decisiones):
├─ API spec (C.1)
├─ BITACORA schema (C.2)
├─ DB schema (C.3)
├─ MVP testing (C.4)
├─ MVP go/no-go (C.5)
├─ Autonomy rules (F.1)
├─ Scoring formula (F.2)
├─ Security review (F.3)
├─ Integration testing (F.4)
├─ v0.5 go/no-go (F.5)
├─ God Mode spec (G.2)
└─ Validaciones & decisiones críticas
```

---

## FLUJO DE EJECUCIÓN RECOMENDADO

**HORA 0 - START:**
1. Vos (Claude): Define C.1, C.2, C.3 (specs arquitectónicas) = 65 min
2. @GEMMA inicia A.1 en paralelo = 45 min
3. @GEMINI espera A.1 (WebSocket live) = 30 min

**HORA ~1 (mientras GEMMA sigue A.2/A.3):**
- @GEMINI: B.1 (React scaffold) = 30 min
- Vos: C.4 (testing plan) = 30 min

**HORA ~2 (A.4 + A.5 listos, B.2+B.3+B.4 paralelo):**
- Testing phase comienza

**MVP 0.01 = LISTO (~2.5-3 hrs pared)**

**FASE 2 (Post MVP):**
- Repite patrón: D.1+D.2+D.4 paralelo → D.3+D.5 → D.6+D.7
- E.1 → E.2+E.3+E.4 paralelo
- F.x validación

**v0.5 = LISTO (~3.5-4 hrs pared)**

---

## NOTAS CRÍTICAS

- ✅ **Sin tiempos humanos** (todo en minutos/horas)
- ✅ **Paralelización máxima** (Gemma + Gemini simultáneo)
- ✅ **Dependencias claras** (qué bloquea qué)
- ✅ **División de trabajo** (cada agente su dominio)
- ✅ **Iterativo** (MVP → 0.5 → v1.0+)
- ⚠️ **Testing es crítico** (C.4, F.4) = no saltear
- ⚠️ **Go/no-go decisions** (C.5, F.5) = Javi aprueba antes de siguiente fase

---

## DEFINICIONES CLAVE

**Room:**
- Espacio de trabajo colaborativo
- Contiene: chat, tablero de tareas, agentes
- Memory compartida (pero cada agente su BITACORA)

**Proyecto:**
- Room con líder
- Líder = user o agente Lead
- Tareas distribuidas

**SOUL.md:**
- Identidad del agente (quién soy, skills, insignias)
- Archivo persistente por agente

**BITACORA.md:**
- Experiencia/historial del agente
- Qué hice, cuándo, resultados
- Transferible entre rooms

**Presupuesto T1:**
- USD/mes por agente Haiku
- Tracking por tarea
- Usuario controla límite

**Score:**
- Tareas exitosas = +1 punto
- Tarea falla = -N puntos (penalización)
- Cada 10 exitosas = insignia

---

## RIESGOS & MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| CPU/GPU bottleneck multi-user | MEDIA | ALTO | Testing PoC, monitoreo |
| Race conditions (agentes simultáneos) | MEDIA | ALTO | Message queue (v0.5) |
| Agentes "zombies" (cuelgados) | ALTA | MEDIO | Healthcheck + systemd restart |
| Memory explosion (BITACORA muy grande) | BAJA | MEDIO | Rotación de logs, archivado |
| Infiltración (agente malicioso) | BAJA | CRÍTICO | Sandboxing + API keys |

---

## MÉTRICAS DE ÉXITO

**MVP (0.01):**
- ✅ Room funcional con 2 agentes
- ✅ Task asignación → ejecución → done
- ✅ Chat con @mentions
- ✅ Memory persiste

**Multi-agente (0.5):**
- ✅ Agentes se comunican entre sí (T0+T2)
- ✅ Scorings y insignias funcionales
- ✅ Multi-user sin crashes

**v1.0:**
- ✅ Topología visual (cables + drag & drop)
- ✅ God Mode operativo
- ✅ Auditoría completa
- ✅ Health dashboard

---

## NEXT STEPS

1. **Decide:** ¿Confirmás plan? ¿Cambios?
2. **Setup:** Crea repo (GitHub/local)
3. **Comenzá:** Backend scaffold (FastAPI + SQLite)
4. **Paralelo:** React frontend (componentes base)
5. **Integración:** Wire up WebSocket

**¿Iniciamos?**
