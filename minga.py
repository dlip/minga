#!/usr/bin/python
import os
import sys
import re
import jinja2
import json
from os import walk

totalArgs = len(sys.argv)

if totalArgs < 4:
  print "Missing arguments"
  print "python minga.py layoutDir templateDir outputDir JsonDefaultOptions JsonOptions"
  exit(1)

for path in [sys.argv[1], sys.argv[2]]:
  if not os.path.isdir(path):
    print "%s is not a folder" % path
    exit(1)

layoutDir = sys.argv[1]
templateDir = sys.argv[2]

templateVars = {}
if totalArgs > 4 and len(sys.argv[4]) > 0:
  templateVars = json.loads(sys.argv[4])
  if totalArgs > 5 and len(sys.argv[5]) > 0:
    templateVars = dict(templateVars.items() + json.loads(sys.argv[5]).items())

outputDir = sys.argv[3]
if not os.path.exists(outputDir):
  os.makedirs(outputDir)

templateLoader = jinja2.FileSystemLoader( [ layoutDir, templateDir ] )
templateEnv = jinja2.Environment( loader=templateLoader )


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
