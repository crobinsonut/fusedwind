
import unittest
from fusedwind.interface import base, _implement_base, implement_base
from openmdao.main.datatypes.api import Float, Slot
from openmdao.main.api import Component, Assembly

class FrameworkTest(unittest.TestCase):
    def testImplements(self):
        for cls_type in [Component, Assembly]:
            @base
            class BaseClass1(cls_type):
                vi1 = Float(iotype='in')
                vi2 = Float(iotype='in')
                vo1 = Float(iotype='out')

            @_implement_base(BaseClass1)
            class MyClass(cls_type):    
                vi1 = Float(iotype='in')
                vi2 = Float(iotype='in')
                vo1 = Float(iotype='out')

            @base
            class BaseClass2(cls_type):
                vi3 = Float(iotype='in')
                vi4 = Float(iotype='in')
                vo2 = Float(iotype='out')


            @implement_base(BaseClass1, BaseClass2)
            class MyClass(cls_type):
                vi1 = Float(iotype='in')
                vi2 = Float(iotype='in')
                vi3 = Float(iotype='in')
                vi4 = Float(iotype='in')

                vo1 = Float(iotype='out')
                vo2 = Float(iotype='out')

            myinst = MyClass()


    def testMixingCompAss(self):
        """Mixing components and assemblies"""

        @base
        class BaseClass1(Component):
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vo1 = Float(iotype='out')

        @base
        class BaseClass2(Component):
            vi3 = Float(iotype='in')
            vi4 = Float(iotype='in')
            vo2 = Float(iotype='out')


        @implement_base(BaseClass1, BaseClass2)
        class MyClass(Assembly):
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vi3 = Float(iotype='in')
            vi4 = Float(iotype='in')

            vo1 = Float(iotype='out')
            vo2 = Float(iotype='out')

        myinst = MyClass()


    def testExtendingIOs(self):
        """Extending the number of inputs and outpus"""

        @base
        class BaseClass1(Component):
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vo1 = Float(iotype='out')

        @implement_base(BaseClass1)
        class MyClass(Component):
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vi3 = Float(iotype='in')
            vi4 = Float(iotype='in')

            vo1 = Float(iotype='out')
            vo2 = Float(iotype='out')

        myinst = MyClass()


    def testExternalConfigure(self):
        """Testing having external configure functions"""

        @base
        class BaseClass1(Component):
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vo1 = Float(iotype='out')


        @implement_base(BaseClass1)
        class C1(Component):
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vo1 = Float(iotype='out')

            def execute(self):
                self.vo1 = self.vi1 + self.vi2

        def configure_C1(self):
            self.add('c1', C1())
            self.connect('vi1', 'c1.vi1')
            self.connect('vi2', 'c1.vi2')
            self.connect('c1.vo1', 'vo1')
            self.driver.workflow.add('c1')

        @base
        class BaseClass2(Component):
            vi1 = Float(iotype='in')
            vi3 = Float(iotype='in')
            vo2 = Float(iotype='out')

        @implement_base(BaseClass2)
        class C2(Component):
            vi1 = Float(iotype='in')
            vi3 = Float(iotype='in')
            vo2 = Float(iotype='out')

            def execute(self):
                self.vo2 = self.vi1 * self.vi3

        def configure_C2(self):
            self.add('c2', C2())
            self.connect('vi1', 'c2.vi1')
            self.connect('vi3', 'c2.vi3')
            self.connect('c2.vo2', 'vo2')
            self.driver.workflow.add('c2')


        @implement_base(BaseClass1, BaseClass2)
        class MyClass(Assembly):
            """Assembly that nests a C1 and C2 component 
            and complies to both base classes I/Os
            """
            vi1 = Float(iotype='in')
            vi2 = Float(iotype='in')
            vi3 = Float(iotype='in')            

            vo1 = Float(iotype='out', desc='vi1+vi2')
            vo2 = Float(iotype='out', desc='vi1*vi3')

            def configure(self):
                configure_C1(self)
                configure_C2(self)                


        from random import random
        myinst = MyClass()
        myinst.vi1 = random()
        myinst.vi2 = random()
        myinst.vi3 = random()   
        myinst.run()
        self.assertEqual(myinst.vo1, myinst.vi1 + myinst.vi2) 
        self.assertEqual(myinst.vo2, myinst.vi1 * myinst.vi3) 





if __name__ == "__main__":
    unittest.main()             