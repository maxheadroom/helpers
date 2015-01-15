#!/bin/bash -x
# this script will extract the validity dates of the SSL certificate 
# usage: check_certificate_dates.sh <domainname>

echo | openssl s_client -connect $1:443 2>/dev/null | openssl x509 -noout -dates