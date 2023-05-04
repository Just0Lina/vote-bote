.PHONY:drop_tables show_tables create_tables
DB=postgres

show_tables:
	@psql -d $(DB) -f show_tables.sql

create_tables:
	@psql -d $(DB) -f create_tables.sql

drop_tables:
	@psql -d $(DB) -f delete_tables.sql
