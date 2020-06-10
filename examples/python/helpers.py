import pprint

def tabulate_data_matrix(data):
    col_width = [max(len(x)+2 for x in col) for col in zip(*data)]
    tabulated_data = ""
    for row in data:
        tabulated_data += "| " + " | ".join("{:{}}".format("\""+x+"\"", col_width[i]) for i, x in enumerate(row)) + "\n"

    return tabulated_data

def pretty_symbols(symbols):
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
    tabulated_symbols += tabulate_data_matrix(is_user_symbols)
    tabulated_symbols += "\n- not is_user:\n"
    tabulated_symbols += tabulate_data_matrix(not_is_user_symbols)

    return tabulated_symbols

def pretty_sections(sections):
  pp = pprint.PrettyPrinter(indent=4)
  return pp.pformat(sections)

def write_output(path, content):
  FILE = open(path, "w")
  FILE.write(content)
  FILE.close()
