#!/usr/bin/env python3

import os
import sys

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../..'
sys.path.insert(0, PROJECT_PATH)

from fract4d_compiler import fc
from fract4d import fractconfig

INPUT_FRACT_CONFIG = fractconfig.userConfig()
INPUT_FORMULA_FILE = "gf4d.frm"
INPUT_FORMULA_NAME = "Mandelbrot"
OUTPUT_PATH = "examples/output/"
OUTPUT_C_FILE = OUTPUT_PATH + INPUT_FORMULA_NAME + ".c"


COMPILER = fc.Compiler(INPUT_FRACT_CONFIG)
FORMULA_IR = COMPILER.get_formula(INPUT_FORMULA_FILE, INPUT_FORMULA_NAME)
LIBRARY_CG = COMPILER.compile(FORMULA_IR)

LIBRARY_CG.output_decls(FORMULA_IR)
C_CODE = LIBRARY_CG.output_c(FORMULA_IR)

FILE = open(OUTPUT_C_FILE, "w")
FILE.write(C_CODE)
FILE.close()


print("Look here for the generated C code  => " + OUTPUT_C_FILE)
