#!/usr/bin/env python3

import os
import sys
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../..'
sys.path.insert(0, PROJECT_PATH)
from fract4d_compiler import fc
from fract4d import fractconfig, fract4dc
from fract4d.tests.fractalsite import FractalSite
from fract4d.fract4d_new.image_wrapper import ImageWrapper
from helpers import pretty_symbols


INPUT_FRACT_CONFIG = fractconfig.userConfig()
INPUT_FORMULA_FILE = "gf4d.frm"
INPUT_FORMULA_NAME = "Mandelbrot"
INPUT_LOCATION_PARAMS = [
    0.0, 0.0, 0.0, 0.0, # X Y Z W
    4.0, # Size or zoom
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0 # XY XZ XW YZ YW ZW planes
]
INPUT_COLOR_MAP = [
    (0.0, 0, 0, 0, 255),
    (1 / 256.0, 255, 255, 255, 255),
    (1.0, 255, 255, 255, 255)
]
OUTPUT_PATH = "examples/output/"
OUTPUT_PNG_FILE = OUTPUT_PATH + INPUT_FORMULA_NAME + ".png"
OUTPUT_SO_FILE = OUTPUT_PNG_FILE + ".so"
OUTPUT_C_FILE = OUTPUT_SO_FILE + ".c"
OUTPUT_SYMBOLS_AFTER_FILE = OUTPUT_C_FILE + ".symbols2"
OUTPUT_SYMBOLS_BEFORE_FILE = OUTPUT_SYMBOLS_AFTER_FILE + ".symbols1"
OUTPUT_IR_FILE = OUTPUT_SYMBOLS_BEFORE_FILE + ".ir"

COMPILER = fc.Compiler(INPUT_FRACT_CONFIG)
MESSAGE_HANDLER = FractalSite()
COLOR_MAP = fract4dc.cmap_create(INPUT_COLOR_MAP)
IMAGE_WRAPPER = ImageWrapper(640, 480)

FORMULA_IR = COMPILER.get_formula(INPUT_FORMULA_FILE, INPUT_FORMULA_NAME)
FILE = open(OUTPUT_IR_FILE, "w")
FILE.write(FORMULA_IR.pretty())
FILE.close()
FILE = open(OUTPUT_SYMBOLS_BEFORE_FILE, "w")
FILE.write(pretty_symbols(FORMULA_IR.symbols))
FILE.close()

LIBRARY_CG = COMPILER.compile(FORMULA_IR)
FILE = open(OUTPUT_SYMBOLS_AFTER_FILE, "w")
FILE.write(pretty_symbols(FORMULA_IR.symbols))
FILE.close()

COMPILER.generate_code(FORMULA_IR, LIBRARY_CG, OUTPUT_SO_FILE, OUTPUT_C_FILE)
FORMULA_PARAMS = FORMULA_IR.symbols.default_params()
CONTROLLER = fract4dc.create_controller(OUTPUT_SO_FILE,
                                        FORMULA_PARAMS,
                                        INPUT_LOCATION_PARAMS)
CONTROLLER.set_message_handler(MESSAGE_HANDLER)
CONTROLLER.start_calculating(
    params=INPUT_LOCATION_PARAMS,
    antialias=0,
    maxiter=100,
    yflip=0,
    nthreads=1,
    cmap=COLOR_MAP,
    auto_deepen=0,
    periodicity=1,
    render_type=0,
    image=IMAGE_WRAPPER.get_img(),
)
IMAGE_WRAPPER.save(OUTPUT_PNG_FILE)

print("Look here for tree-structured intermediate code => " + OUTPUT_IR_FILE)
print("Look here for symbols before compile formula    => " + OUTPUT_SYMBOLS_BEFORE_FILE)
print("Look here for symbols after compile formula     => " + OUTPUT_SYMBOLS_AFTER_FILE)
print("Look here for the generated C code              => " + OUTPUT_C_FILE)
print("Look here for the generated SO code             => " + OUTPUT_SO_FILE)
