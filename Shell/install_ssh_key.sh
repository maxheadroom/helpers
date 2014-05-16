#!/bin/sh -x


host=$1


if [ $# -eq 2 ]; then
		key=$1
		if [ -f $key ]; then
			shift
			host=$1
			cat $key | ssh $host "(tee > ~/public.key; mkdir ~/.ssh; chmod 0700 ~/.ssh; cat ~/public.key >> ~/.ssh/authorized_keys; chmod 0600 ~/.ssh/authorized_keys; ln -s ~/.ssh/authorized_keys ~/.ssh/authorized_keys2 )"
		else
			shift
			key=$1
			cat $key | ssh $host "(tee > ~/public.key; mkdir ~/.ssh; chmod 0700 ~/.ssh; cat ~/public.key >> ~/.ssh/authorized_keys; chmod 0600 ~/.ssh/authorized_keys; ln -s ~/.ssh/authorized_keys ~/.ssh/authorized_keys2 )"
		fi
elif [ $# -eq 1 ]; then
	cat ~/.ssh/id_dsa.pub | ssh $host "(tee > ~/public.key; mkdir ~/.ssh; chmod 0700 ~/.ssh; cat ~/public.key >> ~/.ssh/authorized_keys; chmod 0600 ~/.ssh/authorized_keys; ln -s ~/.ssh/authorized_keys ~/.ssh/authorized_keys2 )"
else
	echo "Usage: $0 keyfile host | host"
fi
