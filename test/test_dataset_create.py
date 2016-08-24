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
import math

import config

if config.get("use_h5py"):
    print("use_h5py")
    import h5py
else:
    import h5pyd as h5py

from common import ut, TestCase
from datetime import datetime
import six


class TestCreateDataset(TestCase):
    def test_create_simple_dset(self):
        filename = self.getFileName("create_simple_dset")
        print("filename:", filename)
        f = h5py.File(filename, "w")

        dims = (40, 80)
        dset = f.create_dataset('simple_dset', dims, dtype='f4')
        
        self.assertEqual(dset.name, "/simple_dset")
        self.assertTrue(isinstance(dset.shape, tuple))
        self.assertEqual(dset.shape[0], 40)
        self.assertEqual(dset.shape[1], 80)
        self.assertEqual(str(dset.dtype), 'float32')
        self.assertTrue(isinstance(dset.maxshape, tuple))
        self.assertEqual(dset.maxshape[0], 40)
        self.assertEqual(dset.maxshape[1], 80)
         
        dset_ref = f['/simple_dset']
        self.assertTrue(dset_ref is not None)
        if not config.get("use_h5py"):
            # obj ids should be the same with h5pyd (but not h5py)
            self.assertEqual(dset.id.id, dset_ref.id.id)
            # Check dataset's last modified time
            self.assertTrue(isinstance(dset.modified, datetime))
            self.assertEqual(dset.modified.tzname(), six.u('UTC'))

        f.close()


if __name__ == '__main__':
    ut.main()