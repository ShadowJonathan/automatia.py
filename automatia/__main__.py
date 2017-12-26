import sys
import re

if "-r" in sys.argv:
    pass  # TODO MAKE RESTART PROCESSING
else:
    import cli

    cli.main()
