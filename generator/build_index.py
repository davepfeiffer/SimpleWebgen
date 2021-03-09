#!/usr/bin/python

"""
This script creates an index pages from the index template that includes
all of the articles in the registry
"""

import argparse
import json

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
      description="Adds post information to the site's index template")
  parser.add_argument('template', help="the path to the index template")
  parser.add_argument('--output', '-o', default='index.md',
      help="the index filename to be written")
  parser.add_argument('--article_dir', default='pages',
      help="the path to the html web article outputs")
  parser.add_argument('--drafts', '-d', action='store_true',
      help="flag for including drafts in the index for testing purposes")
  args = parser.parse_args()

  index = None
  with open(args.template, 'r') as template:
    index = template.readlines()

  with open('./generator/article_registry.json', 'r') as registry_file:
    registry = json.loads(registry_file.read())

    articles = []
    for key, val in registry.items():
      articles.append(val)

    articles = sorted(articles, key=lambda x: x["DATE"], reverse=True)

    for art in articles:
      if art["DRAFT"] == "False" or args.drafts == True:
        link = "* {} :: [{}]({})\n\n".format(
            art["DATE"], art["TITLE"], args.article_dir + '/' + art["PAGE"])
        index.append(link)

    index.append("</div></div>\n")

  with open(args.output, 'w') as file:
    file.writelines(index)