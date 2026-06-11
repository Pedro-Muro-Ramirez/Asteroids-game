#!/usr/bin/env bash
# Build the pygbag WebAssembly bundle and stage it in docs/ for GitHub Pages.
#
# Usage:  ./deploy.sh        (build + stage into docs/)
# Then:   git add -A && git commit -m "Update web build" && git push
#
# GitHub Pages serves from the master branch /docs folder.
set -euo pipefail
cd "$(dirname "$0")"

STAGING="webgame"

echo "==> Staging game source in $STAGING/"
rm -rf "$STAGING"
mkdir -p "$STAGING"
# Copy all top-level Python modules (main.py must be among them).
cp ./*.py "$STAGING/"

echo "==> Building WebAssembly bundle with pygbag"
( cd "$STAGING" && uvx --from pygbag pygbag --build main.py )

echo "==> Publishing build into docs/"
rm -rf docs
mkdir -p docs
# Include BOTH archives: pygbag's loader fetches webgame.tar.gz on most hosts
# (e.g. GitHub Pages) and webgame.apk only on itch.io.
cp "$STAGING/build/web/index.html" \
   "$STAGING/build/web/webgame.apk" \
   "$STAGING/build/web/webgame.tar.gz" \
   "$STAGING/build/web/favicon.png" \
   docs/
# .nojekyll stops GitHub Pages (Jekyll) from ignoring files.
touch docs/.nojekyll

echo "==> Done. docs/ updated:"
ls -1 docs/
echo
echo "Next: git add -A && git commit -m 'Update web build' && git push"
