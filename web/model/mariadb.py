import mariadb
import config
import sys

# MariaDB 연결
try:
    conn = mariadb.connect(
        user=config.mariadb_user_id,
        password=config.mariadb_user_pw,
        host=config.mariadb_server_ip,
        port=config.mariadb_server_port,
        database=config.mariadb__database_name
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

