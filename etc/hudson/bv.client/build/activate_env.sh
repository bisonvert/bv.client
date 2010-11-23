#!/usr/bin/env bash
# install .env if in minitage
cwd="/home/sim/minitage/django/bv.client"
project="bv.client"
test_command="/home/sim/minitage/django/bv.client/bin/bvclient.test"
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
xmlreports="/home/sim/minitage/django/bv.client/parts/bvclient.test/testreports"
tested_packages="
bv.client"
# vim:set et sts=4 ts=4 tw=80:
