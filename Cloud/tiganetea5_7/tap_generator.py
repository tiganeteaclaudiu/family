class TAP_Generator():

    def __init__(self,tap_file):
        self.tap_file = tap_file
        self.buffer = ''
        
    def add_testsuite_header(self, suite_name=None, suite_index=None):
        self.buffer += 'ok {} - {}\n'.format(suite_index,suite_name)

    def add_testcase_header(self, case_name=None, case_index=None, status=None):
        self.buffer += '    {} {} - {}\n'.format(status,case_index,case_name)

    def add_testcase_count(self, testcase_count):
        self.buffer += '    1..{}\n'.format(testcase_count)

    def add_testsuite_count(self, testsuite_count):
        self.buffer += '1..{}\n'.format(testsuite_count)

    def add_data_block_start(self):
        self.buffer += '      ---\n'

    def add_data_block_end(self):
        self.buffer += '      ...\n'
   
    def add_key_value(self, key, value, offset=0):
        for i in range(0,offset):
            self.buffer += ' '
        self.buffer += '      {}: {}\n'.format(key,value)

    def add_list_element(self, value):
        self.buffer += '        - {}\n'.format(value)

    def add_nested_list_element(self, key, value, offset=0, device_index=0):
        self.buffer += '        {}:'.format(key)
        self.buffer += '\n'
        self.buffer += '          {}\n'.format(value)
    
    def add_testcase(self, case_status='',case_name='', case_index='', case_parameters={},
                        suite_parameters={}, devices=[], error_message=''):
        self.add_testcase_header(case_name, case_index, case_status)
        device_index = 0
        if case_status == "not ok":
            self.add_data_block_start()
            self.add_key_value('message', error_message)
            self.add_key_value('method_name', case_parameters['method_name'])
            self.add_key_value('devices','')
            for device in devices:
                self.add_key_value(value='', key='DUT{}'.format(device_index), offset=2),
                self.add_key_value(value=device['id'], key='deviceID', offset=4)
                self.add_key_value(value=device['accounts'][0]['username'], key='username', offset=4)
                self.add_key_value(value=device['accounts'][0]['email'], key='email', offset=4)
                device_index += 1

            self.add_key_value('case_parameters','')

            for key,val in case_parameters.items():
                self.add_nested_list_element(key,val)

            self.add_key_value('suite_parameters','')

            for key,val in suite_parameters.items():
                self.add_nested_list_element(key,val)
            
            self.add_data_block_end()

    def export_tap(self):
        print('Exported TAP Test Report file.')
        filename = 'results.tap'
        file = open(filename, 'w')
        file.write(self.buffer)
        file.close()

if __name__=='__main__':
    generator = TAP_Generator('results_generated.tap')

    case_status='not ok'
    case_name='test_case'
    case_index='2'
    case_parameters = {
        'method_name' : 'test_testname',
        'logging_debug' : 'DEBUG',
        'timeout' : '10'
    }
    suite_parameters = {
        'method_name' : 'test_testname',
        'logging_debug' : 'DEBUG',
        'timeout' : '10'
    }
    devices = [{
        'id' : '1234abcd',
        'accounts' : [ {
            'username' : 'test_username1',
            'email' : 'test_email1'
        }]
    },{
        'id' : '5678efgh',
        'accounts' : [ {
            'username' : 'test_username2',
            'email' : 'test_email2'
        }]
    },]
    error_message = 'EXCEPTION AT LINE 20'

    generator.add_testsuite_header(suite_name='TestSuite',suite_index='1')
    generator.add_testcase(case_name='passed_test', case_index='1',case_status='ok')
    generator.add_testcase(case_name=case_name,case_status=case_status,case_index=case_index,
                        case_parameters=case_parameters,suite_parameters=suite_parameters,
                        devices=devices,error_message=error_message)

    generator.add_testcase_count(2)
    generator.add_testsuite_count(1)

    print(generator.buffer)












