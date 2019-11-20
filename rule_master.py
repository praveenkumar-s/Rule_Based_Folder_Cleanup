from datetime import datetime, timedelta
import os
from os import path
import shutil
import sys

class based_on_retention_time():
    def __init__(self, Params, Exclude=[]):
        self.Params = Params
        self.Exclude = Exclude

    def inflate(self):
        self.retention_period = self.Params['retention_period']
        self.retention_units =  self.Params['retention_units']
        self.delete_files_before_date = None
        if(self.retention_units.upper() =='DAYS'):
            self.delete_files_before_date = datetime.now() - timedelta(days= self.retention_period)
        if(self.retention_units.upper() =='WEEKS'):
            self.delete_files_before_date = datetime.now() - timedelta(weeks= self.retention_period)
        if(self.retention_units.upper() =='MONTHS'):
            self.delete_files_before_date = datetime.now() - timedelta(days= self.retention_period*30)
        if(self.retention_units.upper() =='YEARS'):
            self.delete_files_before_date = datetime.now() - timedelta(days= self.retention_period*365)

        if(None in [self.retention_period , self.retention_units , self.delete_files_before_date]):
            raise Exception("Error during date evaluation")


    def mark(self, FolderPath):
        self.inflate()
        result = {}
        items_in_dir = os.listdir(FolderPath)
        items_in_dir_after_exclusion = [x for x in items_in_dir if x not in self.Exclude]
        for objects in items_in_dir_after_exclusion:
            last_modified_date = None
            last_modified_date = path.getmtime( path.join(FolderPath,objects) )
            last_modified_date = datetime.fromtimestamp(last_modified_date)
            TTL = last_modified_date - self.delete_files_before_date
            TTL_seconds = TTL.total_seconds()            
            result[objects]={
                "TTL":TTL_seconds,
                "delete":(TTL_seconds<0)
            }
        return result

    def clean(self,ParentFolderPath,ObjectsToDelete):
        log = {}
        exceptions=[]
        for items in ObjectsToDelete:
            try:
                shutil.rmtree(path.join(ParentFolderPath,items))
                log[ObjectsToDelete]="done"
            except:
                log[ObjectsToDelete]="failed"
                exceptions.append(str(sys.exc_info()))
        return log,exceptions
        
class based_on_size():
    def __init__(self,Params,Exclude=[]):
        self.Params = Params
        self.Exclude = Exclude

    def clean(self):
        pass
