#!/bin/bash
set -e

echo "[+] Configurando o Hermes Agent..."

HERMES_HOME="${HERMES_HOME:-/opt/data}"
mkdir -p "$HERMES_HOME"
# Garante que /workspace (volume compartilhado) seja acessível como workspace padrão
if [ -d /workspace ]; then
    ln -sfn /workspace "$HERMES_HOME/workspace"
fi

if [ ! -z "$API_SERVER_KEY" ]; then
    echo "API_SERVER_ENABLED=true" > "$HERMES_HOME/.env"
    echo "API_SERVER_KEY=$API_SERVER_KEY" >> "$HERMES_HOME/.env"
    echo "API_SERVER_HOST=${API_SERVER_HOST:-0.0.0.0}" >> "$HERMES_HOME/.env"
echo "HERMES_WRITE_SAFE_ROOT=${HERMES_WRITE_SAFE_ROOT:-/opt/data:/workspace}" >> "$HERMES_HOME/.env"
    echo "API_SERVER_CORS_ORIGINS=*" >> "$HERMES_HOME/.env"
fi

# Credenciais opcionais via arquivo/env
# [ ! -z "$OPENAI_API_KEY" ] && echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> "$HERMES_HOME/.env"
# [ ! -z "$OPENROUTER_API_KEY" ] && echo "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" >> "$HERMES_HOME/.env"

export PATH=/opt/hermes/bin:$PATH
export HERMES_HOME

echo "[+] Instalando plugins..."
hermes plugins install hermes-workflows || pip install hermes-workflows || echo "[!] workflows já instalado/falhou"
hermes plugins install qdrant || pip install hermes-plugin-qdrant || echo "[!] qdrant já instalado/falhou"

echo "[+] Configurando Qdrant..."
hermes memory setup --provider qdrant || true

echo "[+] Iniciando Hermes Gateway..."
exec hermes gateway