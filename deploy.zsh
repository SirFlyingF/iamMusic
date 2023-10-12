# Do not reinstall packages everytime and update is there.
# pip3 install -r requirements.txt

# Set environment variables
export IAMM_API_KEY="HelloMufkr"

# host:port
iamm_address="$1"
parts=(${(s/:/)iamm_address})
HOST=${parts[1]}
PORT=${parts[2]}

# UN:PW:HOST:PORT:DB
db_address="$2"
parts=(${(s/:/)db_address})
export DB_STR="${parts[1]}:${parts[2]}@${parts[3]}:${parts[4]}/${parts[5]}"

export IAMM_LOGLEVEL="$3"
export IAMM_LOGFILE_PATH="$4"

wd=$(pwd)
wd=${wd}/${IAMM_LOGFILE_PATH}
mkrdir -p wd


# gevent is used to keep the connection open for streaming.
gunicorn --bind ${HOST}:${PORT} --workers 1 --timeout 0 -k gevent srvCore:app