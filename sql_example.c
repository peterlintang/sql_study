

/*
 * gcc sql_example.c -lsqlite3
 */
#include <stdio.h>
#include <sqlite3.h>

int main(int argc, char *argv[])
{
	int ret = 0;
	sqlite3 *db = NULL;
	sqlite3_stmt *stmt = NULL;

	ret = sqlite3_open(argv[1], &db);
	if (ret != SQLITE_OK)
	{
		printf("open %s failed, ret: %d\n", argv[1], ret);
		return -1;
	}

	ret = sqlite3_prepare_v2(db, "select * from test_1", -1, &stmt, 0);
	if (ret != SQLITE_OK)
	{
		goto out;
	}

	while ((ret = sqlite3_step(stmt)) == SQLITE_ROW)
	{
		int id = sqlite3_column_int(stmt, 0);
		const char *name = sqlite3_column_text(stmt, 1);
		printf("id: %d, name: %s\n", id, name);
	}

out:
	sqlite3_finalize(stmt);

	ret = sqlite3_close(db);
	if (ret != SQLITE_OK)
	{
		printf("close db failed %d\n", ret);
		return -1;
	}

	return 0;
}
