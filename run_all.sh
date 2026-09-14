#!/usr/bin/env bash
# Reproduces every number, table and figure in the manuscript from the two source files.
#
#   bash run_all.sh
#
# Both notebooks are executed in place, so their stored outputs are replaced by
# the ones your run produces. The notebook files therefore change on every run
# and are deliberately not covered by the checksums; the data going in and the
# artefacts coming out are.
set -euo pipefail

python -m pip install -r requirements.txt

sha256sum -c inputs.sha256

jupyter nbconvert --to notebook --execute --inplace main_analysis.ipynb
jupyter nbconvert --to notebook --execute --inplace revision_analyses.ipynb

sha256sum -c outputs.sha256
echo "All outputs reproduced byte for byte."
