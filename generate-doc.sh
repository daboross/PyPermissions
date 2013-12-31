#!/bin/bash
git add -A
git commit
if [[ "$(git log origin/$(git rev-parse --abbrev-ref HEAD)..HEAD --oneline)" ]]; then
    git push "$@"
    git fetch origin
fi

doxygen doxygen.properties
git checkout gh-pages
rm -r dg
mkdir dg
find doxygen/html -mindepth 1 -maxdepth 1 -exec mv {} ./dg/ \;
rm -r doxygen
git add -A
git commit
git push
git checkout master
