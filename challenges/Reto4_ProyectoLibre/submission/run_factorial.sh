#!/usr/bin/env bash
# Experimento factorial 2x2 con 4 semillas = 16 corridas cortas.
#
#   factor 1: red objetivo    (baseline = sin  |  dqn = con)
#   factor 2: manzana         (orig = puede caer sobre el cuerpo  |  fix = corregida)
#
# Cada celda se corre con 4 semillas para poder reportar DISPERSION, no una anecdota.
# Se ejecutan de a PARALELO procesos con 1 hilo de torch cada uno.

set -u
PY="C:/rl-course_EIA_20262/.venv/Scripts/python.exe"
EPISODIOS=300
TOPE_MIN=12
PARALELO=6
OUT="results/multi"

mkdir -p "$OUT"
echo "factorial 2x2 x 4 semillas | $EPISODIOS episodios | $PARALELO en paralelo"
echo "inicio: $(date +%H:%M:%S)"

lanzados=0
for variante in baseline dqn; do
  for manzana in orig fix; do
    for semilla in 0 1 2 3; do
      etiqueta="${variante}_${manzana}_s${semilla}"
      extra=""
      [ "$manzana" = "fix" ] && extra="--fix-apple"

      "$PY" train_snake.py \
        --variant "$variante" $extra \
        --episodes "$EPISODIOS" --max-minutes "$TOPE_MIN" \
        --seed "$semilla" --threads 1 \
        --eval-every 50 \
        --out "$OUT/${etiqueta}.json" > "$OUT/${etiqueta}.log" 2>&1 &

      lanzados=$((lanzados + 1))
      # limitar la concurrencia
      while [ "$(jobs -rp | wc -l)" -ge "$PARALELO" ]; do sleep 2; done
    done
  done
done

wait
echo "fin: $(date +%H:%M:%S)  ($lanzados corridas)"
