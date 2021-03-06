#!/usr/bin/python

"""
This script:
- adds an entry to the article registry
- adds a makefile rule for the article
- creates a bare bones article from the template

This method is fragile because it has no knowledge of what is in Makefile
and cannot recover from a malformed Makefile.

The general idea of this site generator still seems fine, but it should only
assume that the article_registry.json file is valid.
"""

from datetime import date
from shutil import copyfile
import argparse
import json
import os

REG_PATH = './generator/article_registry.json'
MAKE_PATH = './Makefile'

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
      description="Sets up a new article with the static site generator")
  parser.add_argument('title', help="The title of the article")
  parser.add_argument('--filename', '-f', nargs='?',
      help="The article's filename")
  parser.add_argument('--source_dir', default='articles',
      help="The directory containing the markdown article source files")
  args = parser.parse_args()

  # default filename is just the title with underscores instead of spaces
  if not args.filename:
    args.filename = '_'.join(args.title.split(' '))

  # copy files to be modified
  new_reg = None
  new_make = None
  with open(REG_PATH, 'r') as registry:
    new_reg = json.loads(registry.read())
  with open(MAKE_PATH, 'r') as makefile:
    new_make = makefile.readlines()

  # if the file is new add makefile entries
  if not new_reg.get(args.filename):
    # add rule to the makefile
    top_rule = "$(BIN)/{}.html: $(SRC)/{}.md\n".format(args.filename, args.filename)
    bot_rule = "\tpandoc --metadata title=\"FreeTraderSoftware\" --metadata pagetitle=\"{}\" -s -t html5 --output $@ --css ../$(ART_STYLE) $<\n".format(args.title)
    new_make.append("\n")
    new_make.append(top_rule)
    new_make.append(bot_rule)
    # add page to glob
    for i, line in enumerate(new_make):
      if line.startswith('#!eop'):
        new_make.insert(i, 'PAGES += $(BIN)/{}\n'.format(args.filename + '.html'))
        break
    # write changes to file
    with open(MAKE_PATH, 'w') as makefile:
      makefile.writelines(new_make)

  # add entry to the registry file
  reg_entry = {
    "DRAFT": "False",
    "PAGE": args.filename + '.html',
    "SOURCE": args.filename + '.md',
    "TITLE": args.title,
    "DATE": date.today().strftime('%Y-%m-%d')
  }
  new_reg[args.filename] = reg_entry
  with open(REG_PATH, 'w') as registry:
    registry.write(json.dumps(new_reg, indent=2, separators=(',', ': ')))

  art_path = os.path.join(args.source_dir, args.filename + '.md')
  if os.path.isfile(art_path):
    # touch a markdown file in source folder with correct name
    with open(art_path, 'a'):
      pass
  else:
    # create a copy of the template
    copyfile("./templates/article_template.md", art_path)
