#!/bin/bash
# Fonts für Kinderpraxis-Website herunterladen
# Einmal ausführen: bash download_fonts.sh

DIR="$(cd "$(dirname "$0")" && pwd)"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

echo "Lade DM Sans..."
BASE="https://fonts.gstatic.com/s/dmsans"

# Wir holen die URLs direkt aus der Google Fonts CSS
CSS=$(curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300;1,9..40,400;1,9..40,500&family=Newsreader:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap")

# woff2 URLs extrahieren und herunterladen
echo "$CSS" | grep -o 'url(https://[^)]*\.woff2)' | sed 's/url(//;s/)//' | while read url; do
  # Dateiname aus URL ableiten
  fname=$(echo "$url" | grep -o '[a-zA-Z0-9_-]*\.woff2$')
  if [ -n "$fname" ]; then
    curl -sL -A "$UA" "$url" -o "$DIR/$fname"
    echo "✅ $fname"
  fi
done

echo "Fertig!"
