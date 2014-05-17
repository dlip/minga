import os
import sys
import re
import jinja2
from os import walk

totalArgs = len(sys.argv)

if totalArgs < 6:
  print "Missing arguments"
  print "python minga.py layoutDir templateDir outputDir DefaultOptions Options"
  exit(1)

for path in [sys.argv[1], sys.argv[2]]:
  if not os.path.isdir(path):
    print "%s is not a folder" % path
    exit(1)

layoutDir = sys.argv[1]
templateDir = sys.argv[2]

outputDir = sys.argv[3]
if not os.path.exists(outputDir):
  os.makedirs(outputDir)

templateLoader = jinja2.FileSystemLoader( [ layoutDir, templateDir ] )
templateEnv = jinja2.Environment( loader=templateLoader )

templateVars = { "title" : "Test Example",
                         "description" : "A simple inquiry of function." }

for (dirpath, dirnames, filenames) in walk(templateDir):
  templatePath = re.sub(r"^%s" % templateDir, "", dirpath)
  templatePath = re.sub(r"^/", "", templatePath)
  targetDir = os.path.join(outputDir, templatePath)
  if not os.path.exists( targetDir ):
    os.makedirs(targetDir)
  for filename in filenames:
    inputFilename = os.path.join(templatePath, filename )
    outputFilename = os.path.join(outputDir, templatePath, filename )
    outputFilename = re.sub(r"\.jinja$", "", outputFilename)
    print "Writing template %s to %s" % (inputFilename, outputFilename)
    template = templateEnv.get_template( inputFilename )
    outputText = template.render( templateVars )
    file = open(outputFilename, "w")
    file.write(outputText)
    file.close()
