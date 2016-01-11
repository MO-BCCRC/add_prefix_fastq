'''

Created on May 12, 2014

@author: dgrewal

'''
from kronos.utils import ComponentAbstract
import os


class Component(ComponentAbstract):
    """
    the component adds a prefix before the read names in the
    fastq file to ensure that all the read names are unique
    """
    def __init__(self, component_name='add_prefix_fastq',
                 component_parent_dir=None, seed_dir=None):
        self.version = '1.1.6'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name,
                                        component_parent_dir, seed_dir)
        
    def make_cmd(self, chunk = None):
        if not self.args.run_component:
            cmd = 'cp '+self.args.input+' '+self.args.output
            cmd_args = []
            return cmd, cmd_args

        cmd = self.requirements['python'] + ' ' + \
              os.path.join(self.seed_dir, "addPrefixToFastq.py")
        
        cmd_args = ['--infile '+self.args.input,
                    '--outfile '+self.args.output,
                    '--prefix '+self.args.prefix]
	
        return cmd, cmd_args

    def test(self):
        import component_test
        component_test.run()
                    
def _main():
    comp = Component()
    comp.args = component_ui.args
    comp.run()
    comp.test()
    
    
if __name__ == '__main__':
    import component_ui
    _main()
