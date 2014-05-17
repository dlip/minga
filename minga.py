import os
import sys
import jinja2
from os import walk

totalArgs = len(sys.argv)

if totalArgs < 5:
  print "Missing arguments"
  print "python minga.py layoutDir templateDir DefaultOptions Options"
  exit(1)

for path in [sys.argv[1], sys.argv[2]]:
  if not os.path.isdir(path):
    print "%s is not a folder" % path
    exit(1)

layoutDir = sys.argv[1]
templateDir = sys.argv[2]

def processDir(dir, templateEnv, vars):
  for (dirpath, dirnames, filenames) in walk(templateDir):
    for filename in filenames:
      template = templateEnv.get_template( filename )
      outputText = template.render( vars )
      print outputText

templateLoader = jinja2.FileSystemLoader( [ layoutDir, templateDir ] )
templateEnv = jinja2.Environment( loader=templateLoader )

templateVars = { "title" : "Test Example",
                         "description" : "A simple inquiry of function." }

processDir(templateDir, templateEnv, templateVars)
