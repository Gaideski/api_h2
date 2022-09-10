from repositories.persistance import get_case
import json


class Case:
    def __init__(self) -> None:
        self.get_case_ordered()
        pass

    def extract_values(self):
        min_interval = self.case[0]['diff']
        max_interval = self.case[-1]['diff']
        minimum = [x for x in self.case if x['diff'] == min_interval]
        maximum = [x for x in self.case if x['diff'] == max_interval]
        return minimum, maximum

    def get_structured_data(self):
        minimum, maximum = self.extract_values()
        min_json=[]
        max_json=[]
        for data in minimum:
            resp_data={'producer':data['name'],
                        'interval':data['diff'],
                        'previousWin':data['release']-data['diff'],
                        'followingWin':data['release']}
            min_json.append(resp_data)

        for data in maximum:
            resp_data= {'producer':data['name'],
                        'interval':data['diff'],
                        'previousWin':data['release']-data['diff'],
                        'followingWin':data['release']}
            max_json.append(resp_data)
        return json.dumps({'min':min_json,'max':max_json})



    def get_case_ordered(self):
        case = get_case()
        case.sort(key=lambda x: x['diff'])
        self.case = case
