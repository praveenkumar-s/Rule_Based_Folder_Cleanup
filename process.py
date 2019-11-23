import sys
import rule_master
from datetime import datetime
import json


class task():
    def __init__(self,FolderPath, Rule):
        self.FolderPath = FolderPath
        self.Rule= Rule
        self.exclusion=[]
        self.pre_marked_items=Rule["markers"]
        self.new_marked_items=[]
        self.mark_result=None

    def compute_pre_marked(self):
        final = []
        for items in self.pre_marked_items:
            if((datetime.now()-datetime.strptime(items['marked_on'],r'%Y-%m-%d %H:%M:%S.%f')).total_seconds()>24*3600):#TODO format logic to make sure 24 hours have crossed since marking
                final.append(items['name'])
        self.pre_marked_items=final


    def compute_exclusion(self):
        pass

    def perform(self):
        self.compute_pre_marked()
        self.compute_exclusion()
        type_of_rule = self.Rule['type']
        rule_instance = rule_master.get_rule_object(type_of_rule,self.Rule['params'],self.exclusion)
        self.mark_result = rule_instance.mark(self.FolderPath)
        for items in self.mark_result:
            if(items['delete']==True):
                self.new_marked_items.append(items['name'])
        items_to_clean = list(set(self.pre_marked_items) & set(self.new_marked_items))        
        clean_log,clean_exceptions = rule_instance.clean(self.FolderPath,items_to_clean)
        self.new_marked_items=list(set(self.new_marked_items)^set(self.pre_marked_items))
        for items in self.mark_result:
            if(items['name'] not in self.new_marked_items):
                self.mark_result.remove(items)
        return self.mark_result,clean_log,clean_exceptions
        
    
    def report(self):
        pass


if __name__ == "__main__":
    #rule_id= sys.argv[1]
    #rule_data = {} # TODO:LOGIC TO retreive task data from server
    rule_data  = json.load(open('test_data.json','r'))
    
    for items in rule_data['folders']:
        FolderPath = items['path']
        Rule = items['rule']

        action_item = task(FolderPath,Rule)
        d1,d2,d3=action_item.perform()
        print(d1,d2,d3)
        action_item.report()