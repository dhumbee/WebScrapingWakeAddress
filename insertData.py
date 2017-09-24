import os
import sys

def copyData(csv_file, table_name):
	copy_statement = "\"\\copy {} FROM '{}' WITH CSV DELIMITER ',';\" ".format(table_name, csv_file)
	truncate_statement = "\"truncate table public.{};\"".format(table_name)
	path = "C:\\Progra~1\\PostgreSQL\\9.6\\bin\\psql"
	cmd = "{} -U postgres -d Wake_County_Real_Estate -c {}".format(path, copy_statement) 
	tr_cmd = "{} -U postgres -d Wake_County_Real_Estate -c {}".format(path, truncate_statement)   
	tr_rc = os.system(tr_cmd)
	rc = os.system(cmd)
	print(rc)
	
copyData("property.csv", "property")