#!/usr/bin/env bash

# Copyright (C) 2010, Mathieu PASQUET <mpa@makina-corpus.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the <ORGANIZATION> nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
PROJECT="bv.client"
IMPORT_URL="https://subversion.makina-corpus.net/scrumpy/$PROJECT"
cd $(dirname $0)/..
[[ ! -d t ]] && mkdir t
rm -rf t/*
tar xzvf ~/$PROJECT*z -C t
files="
bootstrap.py
buildout-dev.cfg
buildout-prod.cfg
minitage.buildout-dev.cfg
minitage.buildout-prod.cfg
README.*
etc/
share/
minilays/
deliverance/
"
pushd t
    for f in $files;do
        rsync -azv $f ../$f
    done
popd
rsync -azv t/minilays/bv.client/ bisonvert-minilay/
sed -re "/\[buildout\]/ {
aallow-hosts = \${mirrors:allow-hosts}
}" -i etc/base.cfg
sed -re "s/develop=.*/develop=./g" -i etc/project/bv.client.cfg
sed -re "/\[mirrors\]/ {
aallow-hosts = 
a\     *localhost*
a\     *willowrise.org*
a\     *plone.org*
a\     *zope.org*
a\     *effbot.org*
a\     *python.org*
a\     *initd.org*
a\     *googlecode.com*
a\     *plope.com*
a\     *bitbucket.org*
a\     *repoze.org*
a\     *crummy.com*
a\     *minitage.org*
}" -i etc/sys/settings.cfg


# change the media default
sed -re "/\[app:mediaapp\]/,/^\s*$/s#(resource_name=).*.#\1bv/client/staticfiles/#" -i etc/templates/wsgi/paster.ini.in
sed -re "s/(extends=.*)/\1 etc\/sys\/settings-prod.cfg/g" -i buildout-prod.cfg


# vim:set et sts=4 ts=4 tw=0:
