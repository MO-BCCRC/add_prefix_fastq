'''
Created on Jun 17, 2014

@author: dgrewal
##tests for the count_component
'''

import unittest
import component_reqs, component_main
from collections import defaultdict
import os


class args():
    def __init__(self):
        self.input = './component_test/infile'
        self.output = './component_test/outfile'
        self.prefix = 'DG1234'

class check_requirements(unittest.TestCase):
    def setUp(self):
        self.args = args()

    def __get_version_main(self):
        main_stream = open('component_main.py')
        for line in main_stream:
            if 'self.version' in line:
                return eval(line.strip().split('=')[1])
        return None

    def test_version(self):
        main_version = self.__get_version_main() 
        version = component_reqs.version
        
        self.assertNotEqual(main_version, None, 'Could not retrieve the version from component_main')
        self.assertEqual(main_version, version, 'the version in component_main and component_reqs did not match')

    #make sure that the required fields are present in reqs file
    def test_verify_reqs(self):
        try:
            _ = component_reqs.env_vars
            _ = component_reqs.interval_file
            _ = component_reqs.memory
            _ = component_reqs.parallel
            _ = component_reqs.parallel_params
            _ = component_reqs.requirements
            _ = component_reqs.version
            _ = component_reqs.seed_version
        except:
            self.assertEqual(True, False, 'Please complete the requirements file')
        
        try:
            _ = component_reqs.parallel_run
            self.assertEqual(True, False, 'The parallel_run option must be called parallel in compoenent')
        except:
            pass
        try:
            _ = component_reqs.parallel_mode
            self.assertEqual(True, False, 'The parallel_mode option has been removed')
        except:
            pass
    
    def test_make_cmd(self):
        comp = component_main.Component()
        comp.args = self.args
        cmd,cmd_args = comp.make_cmd(chunk=None)
        cmd_args = ' '.join(map(str,cmd_args))
        
        #The actual resulting command:
        real_cmd =  component_reqs.requirements['python'] +' '+ os.path.join(os.path.abspath('./component_seed/'),'addPrefixToFastq.py')
                        
        real_cmd_args = '--infile '+self.args.input+' --outfile '+self.args.output+' --prefix '+self.args.prefix


        #Ensure that the commands match exactly
        self.assertEqual(real_cmd, cmd, 'Please recheck the cmd variable in make_cmd')
        
        #Ensure that each of the args are present in the command args list 
        self.assertEqual(real_cmd_args, cmd_args, 'Please recheck the cmd_args list in make_cmd')
                
    def test_params(self):
        try:
            from component_params import input_files,input_params,output_files,return_value
        except:
            self.assertEqual(True,False,'Please complete the params file')
        try:
            import component_ui   
        except:
            #cannot run this test if running in unittest mode as ui isn't available
            self.assertEqual(True, True, '') 
            return
            
        arg_act = defaultdict(tuple)
        for val in component_ui.parser._actions[1:]:
            arg_act[val.dest] = (val.required,val.default)
            if val.required == None:
                self.assertEqual(val.default, None, 'The optional argument: '+ val.dest+' has no default value')
        
        #merge all the dictionaries together
        params_dict = dict(input_files.items() + input_params.items() + output_files.items())
        
        for dest,(req,default) in arg_act.iteritems():
            if req == True:
                self.assertEqual(params_dict[dest], '__REQUIRED__', 'params and ui dont match')
            else:
                if not params_dict[dest] in [default,None]:
                    self.assertEqual(True, False, 'Please ensure that either default or ' +\
                                     '__OPTIONAL__ flag is provided for: '+params_dict[dest])

    def test_component(self):
        component = component_main.Component()
        component.args = self.args
        component.run()

        import filecmp
        filecmp.cmp('./component_test/outfile', './component_test/outfile_test')

        os.remove(self.args.output)


def run():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    checkreqs = loader.loadTestsFromTestCase(check_requirements)
    
    suite.addTests(checkreqs)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
