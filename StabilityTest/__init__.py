#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
import StabilityTest.controller.adminController
import StabilityTest.controller.caseController
import StabilityTest.controller.logController