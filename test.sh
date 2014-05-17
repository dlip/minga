#!/bin/bash

MINGA_DEFAULT_OPT='{ "title" : "Test Example", "description" : "Default Description." }'
MINGA_OPT='{ "description" : "Overidden description" }'

# Should run with no options
# bash -c "python minga.py fixtures/input/layout fixtures/input/template output"

# Should run with only default options
#bash -c "python minga.py fixtures/input/layout fixtures/input/template output '$MINGA_DEFAULT_OPT'"

# Should run with default and overriden options
bash -c "python minga.py fixtures/input/layout fixtures/input/template output '$MINGA_DEFAULT_OPT' '$MINGA_OPT'"
