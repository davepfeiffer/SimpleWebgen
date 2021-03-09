
ROOT=.
SRC=articles
BIN=pages

ART_STYLE= css/skinned.css

PAGES=
#!eop (end of pages)


#--{ General Rules }------------------------------------------------------------

.PHONY: test clean

all: $(ROOT)/index.html


test: $(ROOT)/test.html
	mv test.html index.html; rm index.md

clean:
	rm $(BIN)/*.html $(ROOT)/index.html $(ROOT)/index.md $(ROOT)/test.md

# The index is the obvious root page to build
$(ROOT)/index.html: $(ROOT)/index.md
	pandoc --metadata title=TestSite -s -t html5 \
	--output index.html --css $(ART_STYLE) index.md

$(ROOT)/index.md: $(PAGES) $(ROOT)/index_template.md
	python generator/build_index.py $(ROOT)/index_template.md -o $@

# Test index with drafts
$(ROOT)/test.html:  $(ROOT)/test.md
	pandoc --metadata title=TestSite -s -t html5 \
	--output test.html --css $(ART_STYLE) test.md

$(ROOT)/test.md: $(PAGES) $(ROOT)/index_template.md
	python generator/build_index.py  -d $(ROOT)/index_template.md -o $@

#--{ Page Rules }---------------------------------------------------------------
