#!bin/bash

# Programe: Destroy all new VM
# Author : Saoming

string=$(xe vm-list is-control-domain=false  params=name-label | egrep -o  "Cloud_Gaming_[0-9]{18}")
echo "Destroying unuse VMs"

IFS='
' read -a names <<< $string

for name in ${names[@]}
do
    echo $name
    uuid=$(xe vm-list params=uuid name-label=$name | egrep -o "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}")
    echo $uuid
    xe vm-destroy uuid=$uuid
done

