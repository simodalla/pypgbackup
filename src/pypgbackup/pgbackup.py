'''
Created on 05/feb/2010

@author: simo
'''

import sys
import os
import ConfigParser
import subprocess
from datetime import datetime

class PgBackup(object):

    def __init__(self, config_file=None, backup_path=None, debug=False, dry_run=False):
        '''
        Constructor
        '''
        d = datetime.now()
        self.now = d.strftime("%d%m%y%H%M%S")
        self.debug = debug
        self.dry_run = dry_run
        
        if config_file is None:
            #print "Errore, nessun file di configurazione"
            raise ValueError("Errore, nessun file di configurazione")
        if not os.path.exists(config_file):
            raise Exception("Errore, il file di configurazione non esiste") 
        
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)
        self.tasks = self.config.sections()
        if len(self.tasks) == 0:
            raise Exception("Errore, il file di configurazione non contiene task validi")
        if backup_path is None:
            self.backup_path = "./py_pg_backup"
        else:
            self.backup_path = backup_path
        self.set_env()
               
    def set_env(self):
        self.cmd_dump = self.get_cmd_path("pg_dump")
        self.cmd_dumpall = self.get_cmd_path("pg_dumpall")
        
    def get_cmd_path(self, command):
        cmd = subprocess.Popen("which " + command, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
        if len(cmd) == 0:
            raise Exception("Error, command %s is not into system." % command)
        else:
            return cmd
     
    def get_tasks(self):
        str = "################################################\n"
        str += "Elenco dei task:\n\n"
        if len(self.tasks) == 0:
            return "Nessun task valido presente nel file di configurazione"
        for task in self.tasks:
            str += "Task: %s - " % task
            if self.config.has_option(task, 'db'):
                str += "Database: %s" % self.config.get(task, 'db')
            else:
                str += "Database: *All*"
            str += "\n"
        return str + "################################################\n"
     
    def run_tasks(self):
        results = []
        task_db= None
        # check sulla directory radice di destinazione dei backup
        if not os.path.exists(self.backup_path) and self.dry_run is False:
            os.makedirs(self.backup_path)
        for task in sorted(self.tasks):
            if self.debug or self.dry_run:
                print "Esecuzione task '%s': " % task
            task_host = self.config.get(task, 'host')
            bkp_dir_host = "%s/%s" % (self.backup_path, task_host)
            # per ogni host su cui fare un backup, viene creata una sottodirectory con il nome
            # dell'host, dove andranno i backup dell'host
            if not os.path.exists(bkp_dir_host) and self.dry_run is False:
                os.mkdir(bkp_dir_host)
            
            cmd = "%s -h %s -U %s"   
            if self.config.has_option(task, 'db') and len(self.config.get(task, 'db')) > 0:
                task_db = self.config.get(task, 'db')
                cmd = cmd % (self.cmd_dump, 
                                 task_host,
                                 self.config.get(task, 'username'))
                try:
                    cmd += " %s" % self.config.get(task, 'options')
                except ConfigParser.NoOptionError:
                    pass
                bkp_file = "%s/%s_%s.tar" % (bkp_dir_host, task_db, self.now)
                cmd += " -Ft %s > %s" % (task_db,bkp_file)
            else:
                cmd = cmd % (self.cmd_dumpall, 
                                 task_host,
                                 self.config.get(task, 'username'))
                try:
                    cmd += " %s" % self.config.get(task, 'options')
                except ConfigParser.NoOptionError:
                    pass
                bkp_file = "%s/%s_all_%s.dump" % (bkp_dir_host, task_host, self.now)
                cmd += " > %s" % bkp_file
                
            if self.debug or self.dry_run:    
                print "\tEsecuzione comando '%s'" % cmd
            if not self.dry_run:
                res = subprocess.Popen(cmd,
                           shell=True, 
                           stdout=open('/dev/null', 'w'), 
                           stderr=subprocess.PIPE).stderr.readlines()
                if len(res) == 0:
                    results.append({task : True})
                else:
                    results.append({task : res})
            else:
                results.append({task : True})
        if self.debug or self.dry_run: 
            print "\n"
        return results
    