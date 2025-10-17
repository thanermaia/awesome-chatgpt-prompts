from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from .storage import FileStorage
from .importer import import_from_csv
from .search import search
from .rag import SimpleIndexer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prompthub")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_import = sub.add_parser("import", help="Importa prompts de CSV")
    p_import.add_argument("csv", help="Caminho para prompts.csv")
    p_import.add_argument("--prefix", default=None)

    p_list = sub.add_parser("list", help="Lista prompts")

    p_search = sub.add_parser("search", help="Busca por texto")
    p_search.add_argument("query")
    p_search.add_argument("--k", type=int, default=10)

    p_retrieve = sub.add_parser("retrieve", help="RAG simples no KB")
    p_retrieve.add_argument("query")
    p_retrieve.add_argument("--k", type=int, default=3)

    args = parser.parse_args(argv)

    if args.cmd == "import":
        n = import_from_csv(args.csv, FileStorage(), args.prefix)
        print(json.dumps({"imported": n}))
        return 0

    if args.cmd == "list":
        storage = FileStorage()
        docs = storage.list()
        for d in docs:
            print(json.dumps({
                "id": d.id,
                "version": d.version,
                "act": d.act,
            }, ensure_ascii=False))
        return 0

    if args.cmd == "search":
        storage = FileStorage()
        results = search(args.query, storage, args.k)
        for doc, score in results:
            print(json.dumps({
                "id": doc.id,
                "version": doc.version,
                "act": doc.act,
                "score": score,
            }, ensure_ascii=False))
        return 0

    if args.cmd == "retrieve":
        idx = SimpleIndexer()
        results = idx.retrieve(args.query, args.k)
        for path, score in results:
            print(json.dumps({"path": path, "score": score}, ensure_ascii=False))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
