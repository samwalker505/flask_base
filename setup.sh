#!/bin/bash
PROJECT="flask_base"
WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv $PROJECT
workon $PROJECT
pip install -t lib/ -r requirements.txt
ln -s ~/Envs/$PROJECT/lib lib
exit 0
