### Git Data Miner
use process_git.py to process miner data and calculate results.

usage: process_git.py [-h] [--db_url DB_URL] directory_path project_name project_branch

```shell
python process_git.py ~/test_repo/.git test_repo master
```

positional arguments:
  directory_path   Path to the .git directory
  project_name     Name of the project
  project_branch   Git Branch

options:
  -h, --help       show this help message and exit
  --db_url DB_URL  Database URL (default: sqlite:///miner_data.db)

### Run the Server
```shell
pip install "fastapi[standard]"
pip install -r requirements.txt
fastapi dev main.py
```

Visit http://127.0.0.1:8000/projects/1 to see the calculated data