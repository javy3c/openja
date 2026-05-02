# Arquitectura y Flujo de Gemini en OPENJA (Zona Cálida)

Esta documentación ilustra cómo está conectado y operando el agente Gemini dentro del ecosistema de OPENJA (Live Bus de la Zona Cálida).

## 1. Diagrama de Componentes (Arquitectura)

Este diagrama muestra los bloques principales y cómo se comunican entre sí. El orquestador (`systemd`) mantiene vivos tanto al Gateway como al Bridge en background.

```mermaid
graph TD
    subgraph Interfaz
        U((Javier / Usuario))
        UI[OPENJA Dashboard<br>openja.html :18794]
    end

    subgraph Core - Zona Cálida
        GW{Gateway / Live Bus<br>zona_calida_gateway.py :18795}
        HIST[(Historial JSONL)]
    end

    subgraph Agente Gemini
        BRIDGE[Gemini Bridge<br>agents/gemini/bridge.py]
        SYS_PROMPT[Identidad<br>SOUL.md / USER.md]
    end

    subgraph Nube
        GEMINI_API((API de Google<br>Gemini 2.5 Flash))
    end

    U -->|Escribe mensaje| UI
    UI <-->|WebSocket bidireccional| GW
    GW <-->|Persistencia| HIST
    
    GW -->|Rutea @gemini MENTION| BRIDGE
    BRIDGE -->|Eventos ACK / PARTIAL / DONE| GW
    
    SYS_PROMPT -.->|Carga de Personalidad| BRIDGE
    BRIDGE <-->|Llamada API Token Hermes| GEMINI_API

    classDef gateway fill:#ff9999,stroke:#333,stroke-width:2px,color:black;
    classDef agent fill:#99ccff,stroke:#333,stroke-width:2px,color:black;
    classDef cloud fill:#ffff99,stroke:#333,stroke-width:2px,color:black;
    classDef ui fill:#99ff99,stroke:#333,stroke-width:2px,color:black;

    class GW gateway;
    class BRIDGE agent;
    class GEMINI_API cloud;
    class UI ui;
```

## 2. Diagrama de Secuencia (Flujo de Mensajes)

Este es el ciclo de vida exacto de un mensaje desde que escribís en el dashboard hasta que recibís la respuesta.

```mermaid
sequenceDiagram
    actor Javi as Javier Boss
    participant UI as OPENJA UI
    participant GW as Zona Cálida Gateway
    participant Bridge as Gemini Bridge
    participant API as Google Gemini API

    Note over GW,Bridge: systemd mantiene ambos corriendo
    
    Bridge->>GW: 1. Conexión WS + REGISTER agent_id: gemini
    GW-->>Bridge: REGISTER_ACK

    Javi->>UI: 2. Escribe "@gemini analizá esto..."
    UI->>GW: 3. WS JSON type: BROADCAST/MENTION
    GW->>Bridge: 4. Rutea MENTION a @gemini
    
    Bridge->>GW: 5. Envía ACK task_id
    GW-->>UI: 6. Muestra status "✓ Recibido"
    
    Note over Bridge: Se inyecta contexto SOUL.md
    Bridge->>API: 7. Request a Gemini 2.5 Flash
    
    Bridge->>GW: 8. Envía PARTIAL progress: 20%
    GW-->>UI: 9. Muestra "🧠 Analizando..."
    
    API-->>Bridge: 10. Devuelve respuesta generada
    
    Bridge->>GW: 11. Envía DONE + Respuesta Final
    GW-->>UI: 12. Broadcast a clientes conectados
    UI-->>Javi: 13. Renderiza respuesta en chat
```

## Consideraciones Técnicas
* **Recuperación:** Si el `bridge.py` crashea o la conexión WS se corta, el loop interno del script intentará reconectar cada 5 segundos. Si el script entero muere, `systemd` lo reinicia.
* **Seguridad:** El Bridge no expone la API Key. La lee internamente de `/home/hal/.hermes/.env`.
