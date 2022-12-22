#! /var/www/html/env/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html')
#sys.stdout = open('output.logs', 'w')
from dashboard import create_app
application = create_app()