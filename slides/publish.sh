#!/bin/bash
set -exo
# quarto preview ageml.qmd --to revealjs --port 6778 --host 0.0.0.0
quarto render --to revealjs
quarto render --to pptx
quarto render --to pdf