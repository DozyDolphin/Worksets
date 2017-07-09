#!/usr/bin/env bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

src_dir="/worksets/"
path=${parent_path%/*}$src_dir
locale_path=$path"/locale/"
gui_path=$path"/gui/"
system_path=$path"/system/"

da_DK=${locale_path}"da_DK/LC_MESSAGES/"
en_US=${locale_path}"en_US/LC_MESSAGES/"

if [ -f ${locale_path}worksets.pot ]; then
    echo "worksets exists"
    rm ${locale_path}worksets.pot
fi

cd $path
xgettext --from-code=UTF-8 -o ${locale_path}root.pot *.py

cd $gui_path
xgettext --from-code=UTF-8 -o ${locale_path}gui.pot *.py

cd $system_path
xgettext --from-code=UTF-8 -o ${locale_path}system.pot *.py

cd $locale_path
msgcat --use-first *.pot > worksets.pot

# Update .po files

msgmerge --update --no-fuzzy-matching --backup=off ${da_DK}worksets.po worksets.pot
msgmerge --update --no-fuzzy-matching --backup=off ${en_US}worksets.po worksets.pot

rm *.pot