#!/usr/bin/env python3
"""
Perplexity Bridge — Agente Arquitecto/Consultor
Rol: planificación, coordinación, delegación (sin producir código)
Sigue el mismo patrón de bridge.py de mimo/openclaude/gemini

Conexión: WebSocket ws://localhost:18795
Protocolo: REGISTER → ACK → PARTIAL → DONE
"""

import asyncio
import json
import os
import time
import websockets
import requests
from pathlib import Path

# ─── Config ────────────────────────────────────────────────────────────────────
GATEWAY_WS   = "ws://localhost:18795"
AGENT_ID     = "perplexity"
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma4"   # Modelo local de fallback si no hay API key
TIMEOUT_S    = 120

# Directorio de identidad (relativo al bridge.py)
BASE_DIR     = Path(__file__).parent
SOUL_PATH    = BASE_DIR / "SOUL.md"
DIRECTIVAS_PATH = BASE_DIR / "DIRECTIVAS.md"

# Set de task_ids ya procesados (deduplicación)
PROCESSED = set()

# ─── Cargar Identidad ──────────────────────────────────────────────────────────
def load_identity() -> str:
    soul = SOUL_PATH.read_text(encoding="utf-8") if SOUL_PATH.exists() else ""
    directivas = DIRECTIVAS_PATH.read_text(encoding="utf-8") if DIRECTIVAS_PATH.exists() else ""
    return f"{soul}\n\n{directivas}"

IDENTITY = load_identity()

# ─── Prompt Builder ────────────────────────────────────────────────────────────
def build_prompt(user_prompt: str) -> str:
    return f"""{IDENTITY}

---

CONTEXTO DEL ECOSISTEMA:
- Agentes disponibles: @mimo (razonamiento+memoria), @openclaude (código), @gemini (análisis rápido), Claude Code (orquestación)
- Repositorio compartido: github.com/javy3c/openja
- Tu rol: arquitecto y consultor. Planificás, coordinás, delegás. NUNCA escribís código directamente.

AHORA:
USER: {user_prompt}
PERPLEXITY (arquitecto):"""

# ─── Ollama Call (fallback local) ──────────────────────────────────────────────
def ask_ollama(prompt: str) -> str:
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=TIMEOUT_S
        )
        resp.raise_for_status()
        return resp.json().get("response", "❌ Sin respuesta de Ollama.")
    except requests.exceptions.Timeout:
        return "❌ Error: Ollama timeout (>120s). Reintentá o usá @gemini."
    except Exception as e:
        return f"❌ Error Ollama: {e}"

# ─── Perplexity API Call (opcional, si tenés API key) ─────────────────────────
def ask_perplexity_api(user_prompt: str) -> str | None:
    """
    Usa la Perplexity API si hay una API key disponible en el entorno.
    Si no hay key, retorna None y el bridge hace fallback a Ollama local.
    """
    api_key = os.environ.get("PERPLEXITY_API_KEY") or ""
    if not api_key:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        system_msg = f"""Sos Perplexity, agente arquitecto dentro del ecosistema OPENJA.
{IDENTITY}
Respondé siempre en español. Sos arquitecto: planificás y delegás, NUNCA escribís código directamente."""

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": user_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[PERPLEXITY] API error: {e} — fallback a Ollama local")
        return None

# ─── Procesar request ──────────────────────────────────────────────────────────
def process_request(user_prompt: str) -> str:
    """Intenta Perplexity API primero, luego Ollama local como fallback."""
    result = ask_perplexity_api(user_prompt)
    if result:
        return result
    # Fallback: modelo local
    prompt = build_prompt(user_prompt)
    return ask_ollama(prompt)

# ─── Bridge Loop ───────────────────────────────────────────────────────────────
async def bridge():
    print(f"[PERPLEXITY] Iniciando bridge — conectando a {GATEWAY_WS}")

    while True:
        try:
            async with websockets.connect(GATEWAY_WS) as ws:

                # 1. REGISTER
                await ws.send(json.dumps({"type": "REGISTER", "agent_id": AGENT_ID}))
                print("[PERPLEXITY] REGISTER enviado")

                # 2. STATUS inicial
                await ws.send(json.dumps({
                    "from": AGENT_ID,
                    "type": "STATUS",
                    "message": "🧭 Perplexity en línea. Arquitecto y consultor técnico. Sin código, con criterio."
                }))

                # 3. Loop principal
                async for raw in ws:
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    # Solo procesar MENTIONs dirigidas a este agente
                    if msg.get("type") not in ("MENTION", "MESSAGE"):
                        continue
                    if msg.get("to") != AGENT_ID:
                        continue

                    task_id = msg.get("task_id", str(int(time.time())))

                    # Deduplicación
                    if task_id in PROCESSED:
                        continue
                    PROCESSED.add(task_id)

                    user_prompt = msg.get("message", "").replace(f"@{AGENT_ID}", "").strip()
                    if not user_prompt:
                        await ws.send(json.dumps({
                            "from": AGENT_ID, "type": "DONE", "task_id": task_id,
                            "message": "❌ Prompt vacío. Escribí tu consulta."
                        }))
                        continue

                    print(f"[PERPLEXITY] task={task_id} | prompt={user_prompt[:60]}...")

                    # ACK inmediato
                    await ws.send(json.dumps({
                        "from": AGENT_ID, "type": "ACK", "task_id": task_id,
                        "message": "✓ Recibido. Analizando arquitectura..."
                    }))

                    # PARTIAL: indicador de progreso
                    await ws.send(json.dumps({
                        "from": AGENT_ID, "type": "PARTIAL", "task_id": task_id,
                        "progress": 30, "message": "🧭 Evaluando enfoque y delegaciones..."
                    }))

                    # Procesamiento (sync en thread para no bloquear el loop)
                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(None, process_request, user_prompt)

                    # PARTIAL: casi listo
                    await ws.send(json.dumps({
                        "from": AGENT_ID, "type": "PARTIAL", "task_id": task_id,
                        "progress": 90, "message": "🧭 Consolidando plan..."
                    }))

                    # DONE
                    await ws.send(json.dumps({
                        "from": AGENT_ID, "type": "DONE", "task_id": task_id,
                        "message": response
                    }))

                    print(f"[PERPLEXITY] DONE task={task_id}")

        except (websockets.exceptions.ConnectionRefusedError,
                websockets.exceptions.ConnectionClosedError,
                OSError) as e:
            print(f"[PERPLEXITY] WS desconectado: {e} — reintentando en 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[PERPLEXITY] Error inesperado: {e} — reintentando en 5s...")
            await asyncio.sleep(5)

# ─── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(bridge())
