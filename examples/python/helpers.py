import pprint

pp = pprint.PrettyPrinter(indent=4)

def tabulate_tuple_list(data):
    # data: <[<tuple>]>
    col_width = [max(len(x)+2 for x in col) for col in zip(*data)]
    tabulated_data = ""
    for row in data:
        tabulated_data += "| " + " | ".join("{:{}}".format("\""+x+"\"", col_width[i]) for i, x in enumerate(row)) + "\n"

    return tabulated_data

def pretty_symbols(symbols):
    # symbols: <fsymbol.T>
    items_is_user = []
    items_not_is_user = []
    for (name, sym) in list(symbols.items()):
        if symbols.is_user(name):
            items_is_user.append((name, sym))
        else:
            items_not_is_user.append((name, sym))

    is_user_symbols = [(str(name), str(sym)) for (name, sym) in items_is_user]
    not_is_user_symbols = [(str(name), str(sym)) for (name, sym) in items_not_is_user]

    tabulated_symbols = "- is_user:\n"
    tabulated_symbols += tabulate_tuple_list(is_user_symbols)
    tabulated_symbols += "\n- not is_user:\n"
    tabulated_symbols += tabulate_tuple_list(not_is_user_symbols)

    return tabulated_symbols

def pretty_translate(translate):
  # translate: <translate.T>
  return translate.pretty()

def pretty_sections(sections):
  # sections: <{str: ir.Seq}>
  pretty_str = ""
  for section in sections:
    pretty_str += "- section: \"" + section + "\"\n"
    pretty_str += sections[section].pretty() + "\n"

  return pretty_str

def pretty_canon_sections(sections):
  # sections: <{str: [ir.Label,ir.Move,ir.Jump]}>
  pretty_str = ""
  for section in sections:
    pretty_str += "- section: \"" + section + "\"\n"
    pretty_str += "".join( ir.pretty() for ir in sections[section] ) + "\n"

  return pretty_str

def pretty_output_sections(instructions):
  # sections: <{str: [instrtuctions.*]}>
  pretty_str = ""
  for section in instructions:
    pretty_str += "- section: \"" + section + "\"\n"
    pretty_str += "".join( instruction.format() for instruction in instructions[section] ) + "\n"

  return pretty_str

def write_output(path, content):
  FILE = open(path, "w")
  FILE.write(content)
  FILE.close()
