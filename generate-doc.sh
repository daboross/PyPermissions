#!/bin/bash
git add -A
git commit
if [[ "$(git log origin/master..HEAD --oneline)" ]]; then
    git push "$@"
    git fetch origin
fi
echo -n "(continue?)"
read
git checkout gh-pages
[[ "$(git rev-parse --abbrev-ref HEAD)" == "gh-pages" ]] || exit
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
