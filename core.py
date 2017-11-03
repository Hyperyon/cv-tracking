#!/usr/bin/python2
# -*- coding: utf-8 -*-

from ftplib import *
import StringIO as sio
import time
import json


config = []

with open('config.json') as f:
    config = json.load(f)

DIR = config['directory']
FILE = config['file_name']


class Ftp:

    '''Manage transfert file.'''

    # ftp transfert only binary file
    # so we need to convert in binary first
    io_stream = sio.StringIO()

    def __init__(self, user, pwd):
        self.ftp = FTP(config['ftp'])
        self.ftp.login(user, pwd)

        self.change_dir()
        self.old_data = self.get_data()

    def change_dir(self):
        self.ftp.cwd(DIR)

    def get_data(self):
        self.ftp.retrbinary('RETR ' + FILE, self.io_stream.write)
        return self.io_stream.getvalue()

    def join_data(self, new_data):
        self.old_data = unicode(self.old_data, 'utf8')
        # Windows console using cp850 encoding char
        new_data = unicode(new_data, 'cp850')
        return self.old_data + '\n' + new_data

    def send_data(self, new_data):
        # encode all unicode data to utf8
        data = (self.join_data(new_data)).encode('utf8')
        self.ftp.storbinary('STOR ' + FILE, sio.StringIO(data))

field = {'date': 'Date',
         'name_job': 'Intitule du poste',
         'reponse': 'Reponse',
         'comment': 'Commentaire',
         'company': 'Societe'}

for key, value in field.iteritems():
    field[key] = raw_input(value+ ' : ')
    print field[key]


if not field['date']:
    field['date'] = time.strftime('%d-%m-%Y')
else:
    field['date'] = field['date'].replace(' ', '-')

    # format date dd-mm-yy to dd-mm-yyyy
    if len(field['date']) == 8:
        field['date'] = field['date'][:6] + '20' + field['date'][-2:]

if not field['reponse']:
    field['reponse'] = unicode('négative','utf8').encode('cp850')

if not field['comment']:
    field['comment'] = ' '

row = field['date'] + '; ' + field['name_job'] + '; '
row += field['company'] + '; ' + field['reponse'] + '; '
row += field['comment']

print(unicode('\nEntrée saisie\n', 'utf8').encode('cp850')+row)

ftp = Ftp(config['user'], config['password'])

if not raw_input('\nConfirmez ? : '):
    ftp.send_data(row)
else:
    print('abort !')
