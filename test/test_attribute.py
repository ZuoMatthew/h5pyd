##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of H5Serv (HDF5 REST Server) Service, Libraries and      #
# Utilities.  The full HDF5 REST Server copyright notice, including          #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################

import numpy as np
import six
import config

if config.get("use_h5py"):
    import h5py
else:
    import h5pyd as h5py

from common import ut, TestCase


class TestAttribute(TestCase):


    def test_create(self):
        filename = self.getFileName("create_attribute")
        print("filename:", filename)
        f = h5py.File(filename, 'w')

        #f.attrs['a1'] = 42  #  to-do fix

        g1 = f.create_group('g1')

        g1.attrs['a1'] = 42
         
        n = g1.attrs['a1']
        self.assertEqual(n, 42)

        self.assertEqual(len(g1.attrs), 1)

        g1.attrs['b1'] = list(range(10))

        # try replacing 'a1'
        g1.attrs['a1'] = 24

        self.assertEqual(len(g1.attrs), 2)
        
        # create an attribute with explict UTF type
        dt = h5py.special_dtype(vlen=str)
        g1.attrs.create('c1', "Hello HDF", dtype=dt)
         
        value = g1.attrs['c1']

        self.assertEqual(value, "Hello HDF")

        # create attribute with as a fixed length string
        g1.attrs.create('d1', np.string_("This is a numpy string"))

        attr_names = []
        for a in g1.attrs:
            attr_names.append(a)
        self.assertEqual(len(attr_names), 4)
        self.assertTrue('a1' in attr_names)
        self.assertTrue('b1' in attr_names)
        self.assertTrue('c1' in attr_names)
        self.assertTrue('d1' in attr_names)

        # create an array attribute
        g1.attrs["ones"] = np.ones((10,))
        arr = g1.attrs["ones"]
        self.assertEqual(arr.shape, (10,))
        for i in range(10):
            self.assertEqual(arr[i], 1)

        # array of strings
        g1.attrs['strings'] = [np.string_("Hello"), np.string_("Good-bye")]
        arr = g1.attrs['strings']
        self.assertEqual(arr.shape, (2,))
        self.assertEqual(arr[0], b"Hello")
        self.assertEqual(arr[1], b"Good-bye")
        #if six.PY3:
        #    self.assertEqual(arr.dtype, h5py.special_dtype(vlen=str))
        #else:
        self.assertEqual(arr.dtype.kind, 'S')
        # TBD - h5serv is returning S11 here for some reason
        #self.assertEqual(arr.dtype, np.dtype("S8"))

        # byte values
        g1.attrs['e1'] = b"Hello"

        # close file
        f.close()




         

if __name__ == '__main__':
    ut.main()




