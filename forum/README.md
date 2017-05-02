## Launching the Forum

### Prerequisites
* Follow the main instructions to launch your Virtual Machine and successfully log in via the `vagrant ssh` command

### Running the Forum
* Once logged in via SSH access shared files at `cd /vagrant`
* Use `ls` to view files in the current directory, the forum directory should be present.
* Type `cd /vagrant/forum` to change into the forum directory project files.
* Use `ls` to view files in the forum directory and check if the `forum.py` file exists.
* If it does exist, run `python forum.py` to serve on localhost.
* View on browser by typing served localhost into URL - eg. http://localhost:8000/)

### PostgreSQL
* To look at the Database for the forum , type `psql forum` (to use the PSQL Database command line generally, type `pqsl`)
* The `\d posts` command displays the columns of the posts table. Use `q` to go back to the psql prompt.
* `\dt` — list all the tables in the database.
* `\dt+` — list tables plus additional information (notably, how big each table is on disk).
* `ctrl + z` to exit psql prompt.


#### References
* PSQL - docs - https://www.postgresql.org/docs/9.4/static/app-psql.html
