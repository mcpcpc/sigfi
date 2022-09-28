#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import os

chdir = '/root'
bind = ':8080'
workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1000 * workers
errorlog = '/tmp/gunicorn.log'
loglevel = 'warning'