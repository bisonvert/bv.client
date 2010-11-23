#!/usr/bin/env bash
# install .env if in minitage
cwd="/opt/minitage/django/bv.client-prod"
project="bv.client"
test_command="/opt/minitage/django/bv.client-prod/bin/bvclient.test"
category="$(basename $(dirname $(dirname $cwd)))"
minibuild="$(basename $cwd)"
hudson=$cwd/etc/hudson
envfile=$cwd/sys/share/minitage/minitage.env
mcfg=$ins/../../etc/minimerge.cfg
if [[ -f $mcfg ]];then
    if [[ ! -e $envfile ]];then    
        easy_install -U minitage.paste
        ../../bin/paster create -t minitage.instances.env $minibuild
    fi
fi
if [[ -e $envfile ]];then    
    source $envfile
fi
xmlreports="/opt/minitage/django/bv.client-prod/parts/bvclient.test/testreports"
tested_packages="
bv.client"
# vim:set et sts=4 ts=4 tw=80:
