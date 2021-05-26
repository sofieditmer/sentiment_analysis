#!/usr/bin/env bash

VENVNAME=sentiment_venv

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

# problems when installing from requirements.txt
pip install ipython
pip install jupyter

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt

# Install spacy model
python -m spacy download en_core_web_sm

deactivate
echo "build $VENVNAME"