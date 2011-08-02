#!/usr/bin/python

from src.globals import *
from src.utils import getDbCursor
from sys import argv

if __name__ == '__main__':
    f = open(argv[1], 'r')
    admin_request = f.read().strip().split('\n')
    
    (conn, cursor) = getDbCursor(admin_db)
    cursor.execute('insert into users values("%s", "%s", "%s");' % (admin_request[0], admin_request[1], admin_request[2]))
    conn.commit()

    cursor.close()
