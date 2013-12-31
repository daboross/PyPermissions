#!/bin/bash
find . -type f -name '*.py' -exec pydoc -w {} \;
git checkout gh-pages
git add -A
git commit
git push
git checkout master
find . -type f -name '*.html' -exec rm -i {} \;
