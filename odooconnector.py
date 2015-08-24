#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################
#
#        Simple odoo connector
#
#           www.studio73.es
#         contacto@studio73.es
#
#######################################
import xmlrpclib,threading

URL = 'http://localhost'
PORT = 8069
USER = 'admin'
PSWD = 'admin'

class odooconnector:

    def __init__(self, db, url=URL, port=PORT, user=USER, pswd=PSWD):
        self.threads = []
        self.url_port = '%s:%s' %(url,port)
        self.db = db
        self.url = url
        self.port = port
        self.user = user
        self.password = pswd
        self.common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url_port))
        self.models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url_port))
        self.uid = self.common.authenticate(self.db, self.user, self.password, {})
    #
    # Basic functions
    #

    def call(self, model=None, ids=[], function=None, args={}):
        """
            :param model: model to read i.e., 'res.partner'
            :type model: string
            :param ids: list of integers (Ids of models)
            :type ids: list
            :param args: Dictionary with function to call arguments
            :type args: dict
        """
        if model and isinstance(model, str):
            res = self.models.execute_kw(self.db, self.uid, self.password, model, function, [ids], args)
            if len(ids) == 1:
                return res[0]
            return res

    def search(self, model=None, domain=[]):
        """
            :param model: model to search i.e., 'res.partner'
            :type model: string
            :param domain: list of conditions
            :type domain: list
        """
        if model and isinstance(model, str):
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'search', [domain])

    def read(self, model=None, ids=[], fields=[]):
        """
            :param model: model to read i.e., 'res.partner'
            :type model: string
            :param ids: list of integers (Ids of models)
            :type ids: list
            :param fields: list of fields to read
            :type fields: list
        """
        if model and isinstance(model, str):
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'read', [ids], {'fields':fields})

    def search_read(self, model=None, domain=[], fields=[]):
        """
            :param model: model to search and read i.e., 'res.partner'
            :type model: string
            :param domain: list of conditions
            :type domain: list
            :param fields: list of fields to read
            :type fields: list
        """
        if model and isinstance(model, str):
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_read', [domain], {'fields':fields})


    def write(self, model=None, ids=[], values={}):
        """
            :param model: model to write i.e., 'res.partner'
            :type model: string
            :param ids: list of integers (Ids of models)
            :type ids: list
            :param values: values dict of new record
            :type values: dict
        """
        if model and isinstance(model, str):
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'write', [ids, values])


    def create(self, model=None, values={}):
        """
            :param model: model to create i.e., 'res.partner'
            :type model: string
            :param values: values dict of new record
            :type values: dict
        """
        if model and isinstance(model, str):
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'create', [values])


    def unlink(self, model=None, ids=[]):
        """
            :param model: model to unlink i.e., 'res.partner'
            :type model: string
            :param ids: list of integers (Ids of models)
            :type ids: list
        """
        if model and isinstance(model, str):
            return self.models.execute_kw(self.db, self.uid, self.password, model, 'unlink', [ids])

    #
    #   TODO: Test and improve!
    #   Threading functions
    #

    def multi_create(self, model=None, values=[], threads=2):
        if model and isinstance(model, str):
            for chunck_list in self._chunks(values,int(len(values)/threads)+1):
                th = threading.Thread(target=self._create_worker,args=(model, chunck_list,))
                self.threads.append(th)
                th.start()

    def threads_join(self):
        for t in self.threads:
            t.join()

    def _create_worker(self, model, values):
        for val in values:
            self.create(model,val)

    def _chunks(self, l, n):
        #Thanks to http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
        n = max(1, n)
        return [l[i:i + n] for i in range(0, len(l), n)]
