#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${DB_NAME:-univ_music}"
DB_USER="${DB_USER:-univ_user}"
DB_PASS="${DB_PASS:-univ_pass}"
DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-3306}"
DB_SOCKET="${DB_SOCKET:-}"
ROOT_USER="${ROOT_USER:-root}"
ROOT_PASS="${ROOT_PASS:-root}"

if [[ -n "$DB_SOCKET" ]]; then
  MYSQL_CMD=(mysql --socket="$DB_SOCKET" -u "$ROOT_USER")
else
  MYSQL_CMD=(mysql -h "$DB_HOST" -P "$DB_PORT" -u "$ROOT_USER")
fi
if [[ -n "$ROOT_PASS" ]]; then
  MYSQL_CMD+=( -p"$ROOT_PASS" )
elif [[ -x "$(command -v sudo)" ]]; then
  MYSQL_CMD=(sudo mysql)
fi

echo "Initialisation de MariaDB pour la base '$DB_NAME'..."

"${MYSQL_CMD[@]}" <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'$DB_HOST' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'$DB_HOST';
FLUSH PRIVILEGES;
SQL

echo "Base de données et utilisateur créés :"
echo "  database = $DB_NAME"
echo "  user = $DB_USER"
echo "  host = $DB_HOST"
echo "  port = $DB_PORT"
echo "Copie ensuite le DATABASE_URL dans ton environnement :"
echo "export DATABASE_URL='mysql+pymysql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME'"
