#!/bin/bash


BACKUPDIR="/opt/PHOTOS/backup/database"
DATESTAMP=`date +"%A-%H"`


# MUSER=''
# MPW=''

source .backup_mysql.conf

if [ -z $MUSER ]; then
	echo "You sure you have your username/password in .backup_mysql.conf file?"
	exit 1
fi

MYSQLBIN=`which mysql`
MYSQLDUMPBIN=`which mysqldump`
BZIP=`which bzip2`

# check if all necessary binaries are in PATH
if [ -z $MYSQLBIN ]; then
	echo "mysql binary not found in PATH"
	exit 1;
fi

if [ -z $MYSQLDUMPBIN ]; then
	echo "mysqldump binary not found in PATH"
	exit 1;
fi

if [ -z $BZIP ]; then
	echo "bzip2 binary not found in PATH"
	exit 1;
fi

# check if BACKUPDIR exists
if [ ! -d $BACKUPDIR ]; then
	echo "$BACKUPDIR is not a directory"
	exit 1
fi

# Create temp backup dir
mkdir $BACKUPDIR/${DATESTAMP}

# common options for mysql dump
DUMPOPTIONS="-h database.explain-it.org -u$MUSER --password=$MPW"
DUMPOPTIONS_STRUCTURE="${DUMPOPTIONS} --triggers --routines --comments --add-drop-database --add-drop-table -d"
DUMPOPTIONS_DATA="${DUMPOPTIONS} --order-by-primary --lock-tables --extended-insert --complete-insert -n -t"
DUMPOPTIONS_TABLE="${DUMPOPTIONS} --order-by-primary --extended-insert --complete-insert"

function backup_tables {
	MYDB=$1
	MYTABLES=`$MYSQLBIN $DUMPOPTIONS -e "use ${MYDB}; show tables;" -b --skip-column-names -s`
    # mkdir $BACKUPDIR/${DATESTAMP}/${MYDB}
	for table in $MYTABLES; do
		echo "Dumping table: ${table} of database: ${MYDB}"
		$MYSQLDUMPBIN $DUMPOPTIONS_TABLE $MYDB $table > $BACKUPDIR/${DATESTAMP}/${MYDB}/${table}.mysql
	done
}

function backup_schema {
	MYDB=$1
	echo "dumping DATABASE structure for $MYDB"
    mkdir $BACKUPDIR/${DATESTAMP}/${MYDB}
	$MYSQLDUMPBIN $DUMPOPTIONS_STRUCTURE -B $MYDB > $BACKUPDIR/${DATESTAMP}/${MYDB}/structure.mysql
}


function compress_backup {
	tar cvfj ${BACKUPDIR}/${DATESTAMP}.backup.tar.bz2 -C ${BACKUPDIR} ${DATESTAMP}/ && rm -rf ${BACKUPDIR}/${DATESTAMP}/

}

# fetch all databasenames from MySQL
DATABASES=`$MYSQLBIN $DUMPOPTIONS -e "show databases;" -b --skip-column-names -s`



if [ $# -eq 1 ]; then
	# dump single database
	backup_schema $1
	backup_tables $1
	compress_backup
else
	# dump every database
	for database in $DATABASES; do
		backup_schema $database
		backup_tables $database
	done
	compress_backup

fi
