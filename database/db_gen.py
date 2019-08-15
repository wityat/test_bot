tables = {}

tables["profile"] = {
	"chat_id": "INT",
	"first_name": "VARCHAR(16)",
	"last_name": "VARCHAR(16)",
	"phone": "BIGINT"
}

from database import Database
if __name__ == "__main__":
	db = Database()
	for table in tables.keys():
		columns = [ "%s %s" % (column, type) for column, type in list(tables[table].items()) ]
		query = "CREATE TABLE {table} ({columns})".format(table=table, columns=", ".join(columns)) # IF NOT EXISTS
		db.query(query)
	db.commit()
	db.close()

