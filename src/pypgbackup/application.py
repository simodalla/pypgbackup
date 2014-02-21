'''
Created on 09/feb/2010

@author: simo
'''

import optparse
import sys
import os
from pgbackup import PgBackup

def main():
    p = optparse.OptionParser(description="""Utility for make total or only single database postgresql backups""",
                                    prog="pypgbackup",
                                    version="0.1",
                                    usage="%prog [-b backup_path] [-n] [-v] config_file ")
    p.add_option("--backup_path", "-b", help="Path to put backup's file", default="/tmp/py_pg_backup")
    p.add_option("--verbose", "-v", help="Verbose modality", action="store_true", default=False)
    p.add_option("--dry-run", "-n", help="Perform a trial run with no make backup made", action="store_true", default=False)            
    options, arguments = p.parse_args()
    
    if not len(arguments) == 1:
        p.print_help()
        sys.exit(1)
    elif not os.path.exists(arguments[0]):
        print "\nConfiguration file '" + arguments[0] + "' NOT exist!!!.\n"
        sys.exit(1)
    if options.dry_run:
        print "***** Trial run - simulate *****\n"
    p = PgBackup(config_file=arguments[0], 
                 backup_path=options.backup_path, 
                 debug=options.verbose, 
                 dry_run=options.dry_run)

    print p.get_tasks()
    results = p.run_tasks()
    for result in results:
        task = result.keys()[0]
        print "Task: %s - Risultato: %s\n" % (task, result[task])
    
if __name__ == '__main__':
    main()