#!/bin/bash
git add -A
git commit
if [[ "$(git log origin/$(git rev-parse --abbrev-ref HEAD)..HEAD --oneline)" ]]; then
    git push "$@"
    git fetch origin
fi
git checkout gh-pages
rm *
git add -A
git commit -m "Auto"
git checkout master
doxygen doxygen.properties
git checkout gh-pages
find doxygen/html -mindepth 1 -maxdepth 1 -exec mv {} ./ \;
rm -r doxygen
git add -A
git commit --amend
git push
git checkout master
