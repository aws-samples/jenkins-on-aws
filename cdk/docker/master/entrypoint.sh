#!/bin/bash -x

echo "ENTRYPOINT" >> /entrypoint.complete

/sbin/tini -- /usr/local/bin/jenkins.sh
