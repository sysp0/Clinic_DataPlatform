#!/bin/bash

echo "========================================"
echo "Starting SQL Server - please wait..."
echo "========================================"

# Wait until SQL Server is ready
until /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -No -C -Q "SELECT 1" > /dev/null 2>&1
do
  echo "SQL Server is not ready. Waiting 5 seconds..."
  sleep 5
done

echo "Good! SQL Server is now ready."

# Copy backup file to a place we can use it
cp /var/opt/mssql/backup/ClinicDB.bk /tmp/ClinicDB.bk

echo "Starting to restore ClinicDB database..."

# Restore the database (only if it does not exist)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -No -C << EOF
IF DB_ID('ClinicDB') IS NULL
BEGIN
    PRINT 'Creating ClinicDB from backup file...'
    RESTORE DATABASE [ClinicDB]
    FROM DISK = '/tmp/ClinicDB.bk'
    WITH REPLACE,
         MOVE 'ClinicDB'      TO '/var/opt/mssql/data/ClinicDB.mdf',
         MOVE 'ClinicDB_log' TO '/var/opt/mssql/data/ClinicDB_log.ldf'
END
ELSE
BEGIN
    PRINT 'ClinicDB already exists. No changes made.'
END
GO
EOF

echo "========================================"
echo "All done! ClinicDB is ready to use."
echo "========================================"