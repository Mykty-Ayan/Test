#!/bin/sh

echo "Waiting for mongo..."

while ! nc -z mongo-db 27017 ; do
    sleep 0.1
done

echo "MongoDB started successfully"

exec "$@"