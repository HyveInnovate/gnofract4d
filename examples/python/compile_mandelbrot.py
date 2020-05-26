#!/usr/bin/env python3
# ignore pylint wrong-import-position
# pylint: disable=C0413

import os
import sys
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../..'
sys.path.insert(0, PROJECT_PATH)

from fract4d_compiler import fc
from fract4d import fractconfig


COMPILER = fc.Compiler(fractconfig.userConfig())

FORMULA_IR = COMPILER.get_formula("gf4d.frm", "Mandelbrot")
LIBRARY_CG = COMPILER.compile(FORMULA_IR)

LIBRARY_CG.output_decls(FORMULA_IR)
C_CODE = LIBRARY_CG.output_c(FORMULA_IR)

FILE = open("examples/output/mandelbrot.c", "w")
FILE.write(C_CODE)
FILE.close()
