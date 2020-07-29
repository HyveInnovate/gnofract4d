#!/usr/bin/env python3

import os
import sys
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../..'
sys.path.insert(0, PROJECT_PATH)
from pathlib import Path
from fract4d_compiler import fc
from fract4d import fractconfig
from helpers import *

INPUT_GENERATE_COMPILER_PHASE_SNAPSHOTS = True
INPUT_FRACT_CONFIG = fractconfig.userConfig()
INPUT_FORMULA_FILE = "gf4d.frm"
INPUT_FORMULA_NAME = "Mandelbrot"
OUTPUT_PATH = "examples/output/"
OUTPUT_C_FILENAME = OUTPUT_PATH + INPUT_FORMULA_NAME + ".c"

for file_to_remove in Path(OUTPUT_PATH).glob(INPUT_FORMULA_NAME + ".c*"):
    file_to_remove.unlink()

COMPILER = fc.Compiler(INPUT_FRACT_CONFIG)

# 1st obtain tree-structured intermediate code:
# > search formula <get_formula()>
#   > get type of formula from file extension <guess_type_from_filename()>
#     < return "translate.T|ColorFunc|Transform|GradientFunc"
#   > get formula tree <get_parsetree()>
#     > get formula file <get_file()>
#       - if formula file loaded before skip next step
#       > load formula file <load_formula_file()>
#         * get file content
#         > parse file <parse_file()>
#           - preprocess file <preprocessor.T()>
#           * parse file <parser.parse()>
#           < return dict of formula trees <{absyn.Node}>
#         - store formula for next uses <{FormulaFile}> (every FormulaFile includes formulas obtained before <{absyn.Node>})
#         < return formula file <FormulaFile>
#       < return the formula file from stored list <FormulaFile>
#     < return from the FormulaFile formulas dict the formula tree desired <absyn.Node>
#   > create formula translate tree using the type guessed at first <translate.T(absyn.Node)>
#     > generate symbols and sections <translate.T.main()>
#       > <translate.TBase.SECTIONNAME()>
#         > <translate.TBase.update_settings()>
#           > <translate.TBase.setlist()>
#             > <translate.TBase.setting()>
#               * generate and update symbols <fsymbol.T>
#           > update sections <translate.TBase.add_to_section()>
#             * generate and update sections <{str:<ir.Seq>}>
#     > generate canon sections <translate.t.canonicalize()>
#       > for every generated section root node (<ir.Seq>) and both limit labels calculate the content of every canon_section <canon.canonicalize()>
#         > <canon.basic_blocks()>
#           - generate Label, Move and Jump blocks
#           < return blocks <[[<ir.Label>,<ir.Move,<ir.Jump>]]>
#         > <canon.schedule_trace()>
#           - generate trace
#           < return trace <[<ir.Label>,<ir.Move,<ir.Jump>]>
#         < return trace <[<ir.Label>,<ir.Move,<ir.Jump>]>
#       * update canon_sections <{str:[<ir.Label>,<ir.Move,<ir.Jump>]}>
#     < return translate tree object <translate.T>
#   < return formula translate tree <translate.T>
FORMULA_T = COMPILER.get_formula(INPUT_FORMULA_FILE, INPUT_FORMULA_NAME)
if INPUT_GENERATE_COMPILER_PHASE_SNAPSHOTS:
  write_output(OUTPUT_C_FILENAME + ".1.get_formula.formula_translate", pretty_translate(FORMULA_T))
  write_output(OUTPUT_C_FILENAME + ".1.get_formula.formula_translate.sections", pretty_sections(FORMULA_T.sections))
  write_output(OUTPUT_C_FILENAME + ".1.get_formula.formula_translate.symbols", pretty_symbols(FORMULA_T.symbols))
  write_output(OUTPUT_C_FILENAME + ".1.get_formula.formula_translate.canon_sections", pretty_canon_sections(FORMULA_T.canon_sections))

# 2nd obtain code generator:
# > compile <compile()>
#   * create code generator using FORMULA_T.symbols
#   > generate code <cg.output_all()>
#     > generate instructions for every canon_section and save them in output_section <output_section()>
#       > <generate_all_code()>
#         -
#       > <emit_label()>
#se mete todo en out y luego se copia a output_sections
#       - insert canon section instructions in his output_sections position <{str,[instructions.*]}>
#     -
#   < return code generator <codegen>
# extiende la tabla de símbolos
# crea listado de instrucciones por sección y las almacena en outputsections
LIBRARY_CG = COMPILER.compile(FORMULA_T)
if INPUT_GENERATE_COMPILER_PHASE_SNAPSHOTS:
  #write_output(OUTPUT_C_FILENAME + ".2.compile.formula_translate", pretty_translate(FORMULA_T))
  #write_output(OUTPUT_C_FILENAME + ".2.compile.formula_translate.sections", pretty_sections(FORMULA_T.sections))
  write_output(OUTPUT_C_FILENAME + ".2.compile.formula_translate.symbols", pretty_symbols(FORMULA_T.symbols))
  #write_output(OUTPUT_C_FILENAME + ".2.compile.formula_translate.canon_sections", pretty_canon_sections(FORMULA_T.canon_sections))
  write_output(OUTPUT_C_FILENAME + ".2.compile.formula_translate.output_sections", pretty_output_sections(FORMULA_T.output_sections))


# generate C code
LIBRARY_CG.output_decls(FORMULA_T)
if INPUT_GENERATE_COMPILER_PHASE_SNAPSHOTS:
  #write_output(OUTPUT_C_FILENAME+".3b1.output_c.formula_translate", pretty_translate(FORMULA_T))
  #write_output(OUTPUT_C_FILENAME+".3b1.output_c.formula_translate.sections", pretty_sections(FORMULA_T.sections))
  #write_output(OUTPUT_C_FILENAME+".3b1.output_c.formula_translate.symbols", pretty_symbols(FORMULA_T.symbols))
  #write_output(OUTPUT_C_FILENAME+".3b1.output_c.formula_translate.canon_sections", pretty_canon_sections(FORMULA_T.canon_sections))
  write_output(OUTPUT_C_FILENAME+".3.output_decls.formula_translate.output_sections", pretty_output_sections(FORMULA_T.output_sections))
C_CODE = LIBRARY_CG.output_c(FORMULA_T)
#if INPUT_GENERATE_COMPILER_PHASE_SNAPSHOTS:
  #write_output(OUTPUT_C_FILENAME+".3b2.output_c.formula_translate", pretty_translate(FORMULA_T))
  #write_output(OUTPUT_C_FILENAME+".3b2.output_c.formula_translate.sections", pretty_sections(FORMULA_T.sections))
  #write_output(OUTPUT_C_FILENAME+".3b2.output_c.formula_translate.symbols", pretty_symbols(FORMULA_T.symbols))
  #write_output(OUTPUT_C_FILENAME+".3b2.output_c.formula_translate.canon_sections", pretty_canon_sections(FORMULA_T.canon_sections))
  #write_output(OUTPUT_C_FILENAME+".3b2.output_c.formula_translate.output_sections", pretty_output_sections(FORMULA_T.output_sections))

write_output(OUTPUT_C_FILENAME, C_CODE)
print("Look here for the generated C code              => " + OUTPUT_C_FILENAME)

if INPUT_GENERATE_COMPILER_PHASE_SNAPSHOTS:
  print("Look snapshots from status of relevant objects after compiler phases => " + OUTPUT_C_FILENAME + ".STEP.PHASE_NAME.OBJECT[.ATTRIBUTE]")
