import sys
from watchfiles import watch, Change
from pathlib import Path
from subprocess import run
import puml_watch_plantuml as puml
import argparse

class Log:
    def __init__(self):
        self.quiet = False

    def print(self, *args, **kwargs):
        if not self.quiet:
            print(*args, **kwargs)

L = Log()

def parse_args(argv):
    parser = argparse.ArgumentParser("puml_watch")
    parser.add_argument("FILES", nargs="+")
    parser.add_argument("--out-dir", "-o", default=".")
    parser.add_argument("--quiet", "-q", action="store_true", help="remove output except from plantuml.")
    return parser.parse_args(argv)


def do_puml(puml_jar, path, out_dir):
    path = str(Path(path).resolve())
    L.print(path, "->", out_dir)
    run(["java", "-jar", puml_jar, path, "-output", out_dir])


def puml_watch(args):
    out_dir = Path(args.out_dir)
    if not out_dir.exists():
        print(f"{out_dir} does not exist.")
        return 1
    try:
        with puml.plantuml_path() as plantuml:
            for changes in watch(*args.FILES):
                for change, path in changes:
                    if change != Change.deleted:
                        do_puml(plantuml, path, out_dir)
    except KeyboardInterrupt:
        pass


def cli():
    args = parse_args(sys.argv[1:])
    L.quiet = args.quiet
    return puml_watch(args)
