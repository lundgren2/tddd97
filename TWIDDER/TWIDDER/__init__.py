from flask import Flask
app = Flask('TWIDDER')
app = Flask(__name__)

import TWIDDER.views
import TWIDDER.database_helper