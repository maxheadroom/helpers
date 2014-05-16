#!/bin/bash

# use openssl to symetrically encrypt/decrypt a file.
# decryption will output to STDOUT only


# bail out of wrong usage

if [ $# != 2 ]; then
  echo "Usage $0 ( enc | dec ) file"
  exit 1
fi

# bail out if desired file is not readible
if [ ! -r $2 ]; then
  echo "The given file is not readable"
  exit 1
fi

case $1 in
    "dec")
        openssl aes-256-cbc -d -a -in $2
       ;;

    "enc")
        openssl aes-256-cbc -a -salt -in $2 -out $2.sec
        ;;
    *)
        echo "Usage $0 ( enc | dec ) file"
        ;;
esac
