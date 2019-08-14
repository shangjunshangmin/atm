# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
import sys
import os
from credit_card_shopping.core import main
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
main.run()


