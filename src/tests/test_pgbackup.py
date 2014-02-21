'''
Created on 05/feb/2010

@author: simo
'''
import sys
import os
import StringIO
from nose.tools import *
from pypgbackup.pgbackup import PgBackup
from unittest import TestCase
from nose.tools import ok_, eq_
from nose.plugins.attrib import attr

path = os.path.abspath(os.path.dirname(__file__))
pgbackup = None
'''
def test_pgbackup_object_want_a_config_file():
    """Se il costruttore non riceve un file di configurazione stampa un errore"""
    sys.stdout=StringIO.StringIO()
    error = "Errore, nessun file di configurazione\n"
    pgbk = PgBackup()
    assert_equal(error, sys.stdout.getvalue())
'''   
   
def setup():   
    global pgbackup
    pgbackup = PgBackup(config_file = path + "/demo.conf")
   
def test_pgbackup_object_want_a_config_file():
    """Se il costruttore non riceve un file di configurazione lancia un eccezzione"""
    assert_raises(ValueError, PgBackup)
    
def test_conf_file_must_exist_on_filestystem():
    assert_raises(Exception, PgBackup, config_file="pippo.conf")
   
def test_pgbackup_must_has_file_conf():   
    ok_(PgBackup(path + "/demo.conf") is not None)
    
def test_pg_conf_file_must_be_not_empty():
    #ok_(len(PgBackup(path + "/demo_fake.conf").tasks) != 0, 
    #    "Il file di configurazione non contiene task validi")
    assert_raises(Exception, PgBackup, config_file=path + "/demo_fake.conf")

@with_setup(setup)    
def test_get_task():
    eq_(len(pgbackup.tasks), 3)

def test_get_task_with_comment():
    pgbackup = PgBackup(path + "/demo_comment.conf")
    eq_(len(pgbackup.tasks), 2)

def test_command_is_not_in_path():
    """Verifica il lancio di un'eccezzione se un comando che serve al programma, non e' nel sistema"""
    assert_raises(Exception, pgbackup.get_cmd_path, "command_not_exist")
 
def test_commands_pgdump_is_in_path():
    pgbackup.set_env()
    ok_(pgbackup.cmd_dump is not None)
    ok_(pgbackup.cmd_dumpall is not None)

@attr('slow')
def test_run_tasks():
    result = [{'aragorn_all' : True}, 
              {'cityware' : True},
              {'pafweb' : True},]
    pgbackup.set_env()
    eq_(pgbackup.run_tasks(), result)
