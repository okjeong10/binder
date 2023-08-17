import json


def convert_json(title, conll_file, json_file):
    docs = []
    sents = []
    toks = []
    tok_ners = []
    ners = []
    doc_count = 0

    for line in conll_file:
        line = line.strip()
        if not line:
            if toks:
                sents.append(toks)
                ners.append(tok_ners)
                tok_ners = []
                toks = []
            continue

        parse_toks = line.split()

        if len(parse_toks) == 4:
            tok, _, _, entity_name = parse_toks
            if tok == '-DOCSTART-':
                if sents:
                    assert(len(sents) == len(ners))
                    out_line = json.dumps({
                        "sentences": sents,
                        "ners": ners,
                        "doc_key": f"conll03_{title}_{doc_count:04}"
                    })
                    json_file.write(out_line + "\n")

                    sents = []
                    ners = []
                    doc_count += 1
                continue
            else:
                if entity_name.startswith('B-'):
                    tok_ners.append([len(toks), len(toks), entity_name[2:]])
                elif entity_name.startswith('I-'):
                    assert(tok_ners[-1][2] == entity_name[2:])
                    tok_ners[-1][1] = len(toks)

                toks.append(tok)

    if sents:
        assert (len(sents) == len(ners))
        out_line = json.dumps({
            "sentences": sents,
            "ners": ners,
            "doc_key": f"conll03_{title}_{doc_count:04}"
        })
        json_file.write(out_line + "\n")

    return docs


def main():
    config = {
        "train": {
            "in": "raw/train.txt",
            "out": "preproc/train.json"
        },
        "dev": {
            "in": "raw/valid.txt",
            "out": "preproc/dev.json"
        },
        "test": {
            "in": "raw/test.txt",
            "out": "preproc/test.json"
        }
    }

    for title, io_conf in config.items():
        with open(io_conf['in'], 'r') as conll_file, open(io_conf['out'], 'w') as json_file:
            convert_json(title, conll_file, json_file)
            print(f'saved to {io_conf["out"]}')


if __name__ == '__main__':
    main()
