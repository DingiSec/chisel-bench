import sys

def main(cf):
    '''
    llvm-cbe will add debug line to each "block", such as #line34 "new.c"
    This script taint this line to every line of the block
    '''
    with open(cf, 'r') as file:
        lines = file.readlines()
    asan_line = ""
    for idx,l_ in enumerate(lines):
        if len(l_) > 2 and l_[-2] == ':': # for label line, such as "_26:"
            continue
        if len(l_.strip()) == 0:
            continue
        if l_[:5] == '#line':
            asan_line = ""
            if "AddressSanitizer.cpp" in l_:
                asan_line = l_.split("/")[-1][:-2]
            continue
        if asan_line:
            lines[idx] = lines[idx][:-1] + " //" + asan_line + "\n"

    with open(cf + ".new", 'w') as file:
        file.write("".join(lines))

if __name__ == "__main__":

    main(sys.argv[1])
