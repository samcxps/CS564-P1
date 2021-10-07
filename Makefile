main:
				sh runParser.sh
				sqlite3 Data.db < create.sql
				sqlite3 Data.db < load.txt

db:
				sqlite3 Data.db < create.sql
				sqlite3 Data.db < load.txt