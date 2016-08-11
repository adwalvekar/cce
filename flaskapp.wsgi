import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/cce.adityawalvekar.com/")
from public_html import app as application
application.debug=True