remote_srv=root@107.174.254.39
remote_srv_workdir=/home/CloudFlare5sBypass


unset LC_CTYPE
rsync -r --exclude="*.pyc" --exclude=".git/" --exclude="logs/"  --exclude="images/" --exclude="cache_data/"  -v ./ ${remote_srv}:${remote_srv_workdir}
