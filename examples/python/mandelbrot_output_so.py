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
OUTPUT_SO_FILE = OUTPUT_PATH + INPUT_FORMULA_NAME + ".so"
OUTPUT_C_FILE = OUTPUT_SO_FILE + ".c"
OUTPUT_IR_FILE = OUTPUT_C_FILE + ".ir"

COMPILER = fc.Compiler(INPUT_FRACT_CONFIG)

FORMULA_IR = COMPILER.get_formula(INPUT_FORMULA_FILE, INPUT_FORMULA_NAME)
FILE = open(OUTPUT_IR_FILE, "w")
FILE.write(FORMULA_IR.pretty())
FILE.close()

LIBRARY_CG = COMPILER.compile(FORMULA_IR)
COMPILER.generate_code(FORMULA_IR, LIBRARY_CG, OUTPUT_SO_FILE, OUTPUT_C_FILE)


print("Look here for tree-structured intermediate code => " + OUTPUT_IR_FILE)
print("Look here for the generated C code              => " + OUTPUT_C_FILE)
print("Look here for the generated SO code             => " + OUTPUT_SO_FILE)
