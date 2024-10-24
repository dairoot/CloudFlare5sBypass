remote_srv=root@107.173.255.100
remote_srv_workdir=/home/CloudFlare5sBypass


unset LC_CTYPE
rsync -r --exclude="*.pyc" --exclude=".git/" --exclude="logs/"  --exclude="image/" --exclude="cache_data/"  ./ ${remote_srv}:${remote_srv_workdir}
