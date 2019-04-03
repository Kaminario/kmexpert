#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

DIR=$(CURDIR)

test:
	touch test.make
	python -m unittest discover
	# remove history file produced by running the tests
	find $(DIR) -name '*.history' -newer $(DIR)/test.make -exec rm {} \;
	find $(DIR) -name '*.pyc' -exec rm {} \;
	rm -f test.make

build: test
	python setup.py sdist