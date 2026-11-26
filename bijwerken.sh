#!/bin/bash
cd ~/koersen || exit 1
git pull -q --rebase
~/koersen-env/bin/python koersen.py > laatste_run.log 2>&1
git add -A
git commit -q -m "Koersen $(date -u +%FT%H:%MZ)" && git push -q
