#!/usr/bin/env bash
# Analisis de sensibilidad al tamano del replay buffer.
#
# Pone a prueba la hipotesis de la seccion 9.1: la inestabilidad del dqn vendria de que el
# buffer guarda solo 1.000 transiciones mientras cada episodio hace 10.000 extracciones,
# de modo que la red se reajusta obsesivamente a una rebanada muy reciente de datos.
#
# Prediccion: si la hipotesis es correcta, agrandar el buffer debe REDUCIR LA VARIANZA
# entre semillas, no necesariamente subir la media.

set -u
PY="C:/rl-course_EIA_20262/.venv/Scripts/python.exe"
EPISODIOS=300
TOPE_MIN=12
PARALELO=6
OUT="results/buffer"

mkdir -p "$OUT"
echo "barrido de buffer | $EPISODIOS episodios | inicio: $(date +%H:%M:%S)"

for buffer in 1000 5000 20000; do
  for semilla in 0 1 2; do
    etiqueta="dqn_buf${buffer}_s${semilla}"
    "$PY" train_snake.py \
      --variant dqn --buffer "$buffer" \
      --episodes "$EPISODIOS" --max-minutes "$TOPE_MIN" \
      --seed "$semilla" --threads 1 --eval-every 50 \
      --out "$OUT/${etiqueta}.json" > "$OUT/${etiqueta}.log" 2>&1 &
    while [ "$(jobs -rp | wc -l)" -ge "$PARALELO" ]; do sleep 2; done
  done
done

wait
echo "fin: $(date +%H:%M:%S)"
