#!/usr/bin/env python
# -*- coding: utf-8 -*-
from StabilityTest import app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
app.config.from_pyfile('settings.py', silent=True)
app.run(debug=True)
