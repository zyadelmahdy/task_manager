# #!/bin/bash
# # wait-for-db.sh

# set -e

# host="$1"
# shift
# cmd="$@"

# until nc -z -v -w30 $host 5432; do
#   echo "Waiting for PostgreSQL at $host to start..."
#   sleep 1
# done

# echo "PostgreSQL is up - executing command"
# exec $cmd