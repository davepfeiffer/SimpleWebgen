This is a simple static site generator using the standard tools: make, python, and pandoc.

Issuing commands from the root the follow actions can be performed easily:

1. __create article__ :: ` python generator/new_article.py 
<article-title> [-f <name-of-file>] [--source_dir <path-source>] `

2. __generate website__ :: ` make `

The following features are not automated but should be:

3. __delete article__

4. __edit article meta data__ (name, date, etc)

The actions can be performed manually, if one understand how the makefile is structured and how the `generator/build_index.py` script works.
