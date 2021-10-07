main:
				sh runParser.sh
				cat dat_files/user.dat | sort | uniq > dat_files/user.dat 
				sqlite3 Data.db < create.sql
				sqlite3 Data.db < load.txt
