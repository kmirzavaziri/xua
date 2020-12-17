import argparse
import re
import os
import shutil

from HtmlGenerator import HtmlGenerator            

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()

parser.add_argument("--custom", action='store_true', help="Customized Doc Generation")
parser.add_argument("-f", "--files", nargs='+', help="Input files", required = True)
parser.add_argument("-t", "--template", nargs=1, help="Template file")

args = parser.parse_args()

# if args.custom:

if args.template:
    templateContent = open(args.template[0], "r").read()
else:
    templateContent = open(dir_path + os.path.sep + "template.html", "r").read()

for fileName in args.files:
    lines = open(fileName, "r").read().splitlines()
    htmlGenerator = HtmlGenerator(lines)
    if htmlGenerator.warnings:
        print('\n'.join(htmlGenerator.warnings))
    html = htmlGenerator.render(templateContent)

    htmlFileName = os.path.splitext(fileName)[0] + ".html"
    open(htmlFileName, "w").write(html)

