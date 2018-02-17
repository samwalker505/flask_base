#!/bin/bash
PROJECT="flask_base"
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
workon $PROJECT && dev_appserver.py --log_level debug .
exit 0
