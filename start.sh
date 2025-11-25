#!/bin/bash

echo "Iniciando API (Mestre)..."
uvicorn backend.app:app --host 0.0.0.0 --port 8000 &

API_PID=$!

echo "Iniciando Interface..."
export API_URL="http://localhost:8000"
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 &

UI_PID=$!

wait $API_PID
EXIT_CODE=$?

echo "⚠️ A API parou ou caiu (Código de saída: $EXIT_CODE). Derrubando o frontend..."
kill $UI_PID
exit $EXIT_CODE