import sys, getopt, sqlite3, datetime

SQL_INSERT = 'INSERT INTO SAMPLES (id, value) VALUES (?,?)'

def main(argv):
    database_file = ''
    try:
        opts, args = getopt.getopt(argv,"hd:",["dbfile="])
    except getopt.GetoptError:
        print('test.py -d <dbfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('samples.py -d <dbfile>')
            sys.exit()
        elif opt in ("-d", "--dbfile"):
            database_file = arg
    
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute(SQL_INSERT, (id,value))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])



