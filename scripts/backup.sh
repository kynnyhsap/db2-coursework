port=40000
backup_path=../data/backup

mongodump --out=$backup_path --host=localhost --port=$port