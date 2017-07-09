#!/usr/bin/env bash

src_dir="/worksets/"
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

path=${parent_path%/*}$src_dir
locale_path=$path"/locale/"

da_DK=${locale_path}"da_DK/LC_MESSAGES/"
en_US=${locale_path}"en_US/LC_MESSAGES/"

# Convert to .mo files

msgfmt ${da_DK}worksets.po -o ${da_DK}worksets.mo
msgfmt ${en_US}worksets.po -o ${en_US}worksets.mo