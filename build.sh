#!/usr/bin/env bash
# Przerwij skrypt w przypadku błędu
set -o errexit

# 1. Instalacja zależności Node.js (np. npm install lub yarn install)
npm install

# 2. Budowanie projektu TypeScript (jeśli używasz buildu do dist/build)
npm run build --if-present

# 3. Pobranie statycznego binarnego FFmpeg, jeśli jeszcze go nie ma
if [ ! -d "ffmpeg" ]; then
  echo "=== Pobieranie FFmpeg ==="
  mkdir ffmpeg
  cd ffmpeg
  curl -L https://johnvansickle.com | tar -xJ --strip-components=1
  cd ..
  echo "=== FFmpeg zainstalowany pomyślnie ==="
fi
