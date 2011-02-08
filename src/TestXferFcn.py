#!/usr/bin/env python

import numpy as np
from xferfcn import xTransferFunction
import unittest

class TestXferFcn(unittest.TestCase):
    """These are tests for functionality and correct reporting of the transfer
    function class.  Throughout these tests, we will give different input
    formats to the xTranferFunction constructor, to try to break it."""
    
    def testTruncateCoeff(self):
        """Remove extraneous zeros in polynomial representations."""
        
        sys1 = xTransferFunction([0., 0., 1., 2.], [[[0., 0., 0., 3., 2., 1.]]])
        
        np.testing.assert_array_equal(sys1.num, [[[1., 2.]]])
        np.testing.assert_array_equal(sys1.den, [[[3., 2., 1.]]])
    
    def testNegScalar(self):
        """Negate a direct feedthrough system."""
        
        sys1 = xTransferFunction(2., np.array([-3]))
        sys2 = - sys1
        
        np.testing.assert_array_equal(sys2.num, [[[-2.]]])
        np.testing.assert_array_equal(sys2.den, [[[-3.]]])
    
    def testNegSISO(self):
        """Negate a SISO system."""
        
        sys1 = xTransferFunction([1., 3., 5], [1., 6., 2., -1.])
        sys2 = - sys1
        
        np.testing.assert_array_equal(sys2.num, [[[-1., -3., -5.]]])
        np.testing.assert_array_equal(sys2.den, [[[1., 6., 2., -1.]]])
        
    def testNegMIMO(self):
        """Negate a MIMO system."""
    
        num1 = [[[1., 2.], [0., 3.], [2., -1.]],
                [[1.], [4., 0.], [1., -4., 3.]]]
        num3 = [[[-1., -2.], [0., -3.], [-2., 1.]],
                [[-1.], [-4., 0.], [-1., 4., -3.]]]
        den1 = [[[-3., 2., 4.], [1., 0., 0.], [2., -1.]],
                [[3., 0., .0], [2., -1., -1.], [1.]]]
                
        sys1 = xTransferFunction(num1, den1)
        sys2 = - sys1
        sys3 = xTransferFunction(num3, den1)
        
        for i in range(sys3.outputs):
            for j in range(sys3.inputs):
                np.testing.assert_array_equal(sys2.num[i][j], sys3.num[i][j])
                np.testing.assert_array_equal(sys2.den[i][j], sys3.den[i][j])
                
    def testAddScalar(self):
        """Add two direct feedthrough systems."""
        
        sys1 = xTransferFunction(1., [[[1.]]])
        sys2 = xTransferFunction(np.array([2.]), [1.])
        sys3 = sys1 + sys2
        
        np.testing.assert_array_equal(sys3.num, 3.)
        np.testing.assert_array_equal(sys3.den, 1.)

    def testAddSISO(self):
        """Add two SISO systems."""
        
        sys1 = xTransferFunction([1., 3., 5], [1., 6., 2., -1])
        sys2 = xTransferFunction([[np.array([-1., 3.])]], [[[1., 0., -1.]]])
        sys3 = sys1 + sys2
        
        # If sys3.num is [[[0., 20., 4., -8.]]], then this is wrong!
        np.testing.assert_array_equal(sys3.num, [[[20., 4., -8]]])
        np.testing.assert_array_equal(sys3.den, [[[1., 6., 1., -7., -2., 1.]]])
        
    def testAddMIMO(self):
        """Add two MIMO systems."""
        
        num1 = [[[1., 2.], [0., 3.], [2., -1.]],
                [[1.], [4., 0.], [1., -4., 3.]]]
        den1 = [[[-3., 2., 4.], [1., 0., 0.], [2., -1.]],
                [[3., 0., .0], [2., -1., -1.], [1.]]]
        num2 = [[[0., 0., -1], [2.], [-1., -1.]],
                [[1., 2.], [-1., -2.], [4.]]]
        den2 = [[[-1.], [1., 2., 3.], [-1., -1.]],
                [[-4., -3., 2.], [0., 1.], [1., 0.]]]
        num3 = [[[3., -3., -6], [5., 6., 9.], [-4., -2., 2]],
                [[3., 2., -3., 2], [-2., -3., 7., 2.], [1., -4., 3., 4]]]
        den3 = [[[3., -2., -4.], [1., 2., 3., 0., 0.], [-2., -1., 1.]],
                [[-12., -9., 6., 0., 0.], [2., -1., -1.], [1., 0.]]]
                
        sys1 = xTransferFunction(num1, den1)
        sys2 = xTransferFunction(num2, den2)
        sys3 = sys1 + sys2

        for i in range(sys3.outputs):
            for j in range(sys3.inputs):
                np.testing.assert_array_equal(sys3.num[i][j], num3[i][j])
                np.testing.assert_array_equal(sys3.den[i][j], den3[i][j])
    
    def testSubScalar(self):
        """Add two direct feedthrough systems."""
        
        sys1 = xTransferFunction(1., [[[1.]]])
        sys2 = xTransferFunction(np.array([2.]), [1.])
        sys3 = sys1 - sys2
        
        np.testing.assert_array_equal(sys3.num, -1.)
        np.testing.assert_array_equal(sys3.den, 1.)

    def testSubSISO(self):
        """Add two SISO systems."""
        
        sys1 = xTransferFunction([1., 3., 5], [1., 6., 2., -1])
        sys2 = xTransferFunction([[np.array([-1., 3.])]], [[[1., 0., -1.]]])
        sys3 = sys1 - sys2
        sys4 = sys2 - sys1
        
        np.testing.assert_array_equal(sys3.num, [[[2., 6., -12., -10., -2.]]])
        np.testing.assert_array_equal(sys3.den, [[[1., 6., 1., -7., -2., 1.]]])
        np.testing.assert_array_equal(sys4.num, [[[-2., -6., 12., 10., 2.]]])
        np.testing.assert_array_equal(sys4.den, [[[1., 6., 1., -7., -2., 1.]]])
        
    def testSubMIMO(self):
        """Add two MIMO systems."""
        
        num1 = [[[1., 2.], [0., 3.], [2., -1.]],
                [[1.], [4., 0.], [1., -4., 3.]]]
        den1 = [[[-3., 2., 4.], [1., 0., 0.], [2., -1.]],
                [[3., 0., .0], [2., -1., -1.], [1.]]]
        num2 = [[[0., 0., -1], [2.], [-1., -1.]],
                [[1., 2.], [-1., -2.], [4.]]]
        den2 = [[[-1.], [1., 2., 3.], [-1., -1.]],
                [[-4., -3., 2.], [0., 1.], [1., 0.]]]
        num3 = [[[3., -3., -6], [5., 6., 9.], [-4., -2., 2]],
                [[3., 2., -3., 2], [-2., -3., 7., 2.], [1., -4., 3., 4]]]
        den3 = [[[3., -2., -4.], [1., 2., 3., 0., 0.], [-2., -1., 1.]],
                [[-12., -9., 6., 0., 0.], [2., -1., -1.], [1., 0.]]]
                
        sys1 = xTransferFunction(num1, den1)
        sys2 = xTransferFunction(num2, den2)
        sys3 = sys1 + sys2

        for i in range(sys3.outputs):
            for j in range(sys3.inputs):
                np.testing.assert_array_equal(sys3.num[i][j], num3[i][j])
                np.testing.assert_array_equal(sys3.den[i][j], den3[i][j])
                
    def testMulScalar(self):
        """Multiply two direct feedthrough systems."""
        
        sys1 = xTransferFunction(2., [1.])
        sys2 = xTransferFunction(1., 4.)
        sys3 = sys1 * sys2
        sys4 = sys1 * sys2
        
        np.testing.assert_array_equal(sys3.num, [[[2.]]])
        np.testing.assert_array_equal(sys3.den, [[[4.]]])
        np.testing.assert_array_equal(sys3.num, sys4.num)
        np.testing.assert_array_equal(sys3.den, sys4.den)
        
    def testMulSISO(self):
        """Multiply two SISO systems."""
        
        sys1 = xTransferFunction([1., 3., 5], [1., 6., 2., -1])
        sys2 = xTransferFunction([[[-1., 3.]]], [[[1., 0., -1.]]])
        sys3 = sys1 * sys2
        sys4 = sys2 * sys1
        
        np.testing.assert_array_equal(sys3.num, [[[-1., 0., 4., 15.]]])
        np.testing.assert_array_equal(sys3.den, [[[1., 6., 1., -7., -2., 1.]]])
        np.testing.assert_array_equal(sys3.num, sys4.num)
        np.testing.assert_array_equal(sys3.den, sys4.den)
        
    def testMulMIMO(self):
        """Multiply two MIMO systems."""
        
        num1 = [[[1., 2.], [0., 3.], [2., -1.]],
                [[1.], [4., 0.], [1., -4., 3.]]]
        den1 = [[[-3., 2., 4.], [1., 0., 0.], [2., -1.]],
                [[3., 0., .0], [2., -1., -1.], [1.]]]
        num2 = [[[0., 1., 2.]],
                [[1., -5.]],
                [[-2., 1., 4.]]]
        den2 = [[[1., 0., 0., 0.]],
                [[-2., 1., 3.]],
                [[4., -1., -1., 0.]]]
        num3 = [[[-24., 52., -14., 245., -490., -115., 467., -95., -56., 12.,
                  0., 0., 0.]],
                [[24., -132., 138., 345., -768., -106., 510., 41., -79., -69.,
                -23., 17., 6., 0.]]]
        den3 = [[[48., -92., -84., 183., 44., -97., -2., 12., 0., 0., 0., 0.,
                  0., 0.]],
                [[-48., 60., 84., -81., -45., 21., 9., 0., 0., 0., 0., 0., 0.]]]
        
        sys1 = xTransferFunction(num1, den1)
        sys2 = xTransferFunction(num2, den2)
        sys3 = sys1 * sys2
        
        for i in range(sys3.outputs):
            for j in range(sys3.inputs):
                np.testing.assert_array_equal(sys3.num[i][j], num3[i][j])
                np.testing.assert_array_equal(sys3.den[i][j], den3[i][j])

    def testDivScalar(self):
        """Divide two direct feedthrough systems."""
        
        sys1 = xTransferFunction(np.array([3.]), -4.)
        sys2 = xTransferFunction(5., 2.)
        sys3 = sys1 / sys2
        
        np.testing.assert_array_equal(sys3.num, [[[6.]]])
        np.testing.assert_array_equal(sys3.den, [[[-20.]]])
        
    def testDivSISO(self):
        """Divide two SISO systems."""
        
        sys1 = xTransferFunction([1., 3., 5], [1., 6., 2., -1])
        sys2 = xTransferFunction([[[-1., 3.]]], [[[1., 0., -1.]]])
        sys3 = sys1 / sys2
        sys4 = sys2 / sys1
        
        np.testing.assert_array_equal(sys3.num, [[[1., 3., 4., -3., -5.]]])
        np.testing.assert_array_equal(sys3.den, [[[-1., -3., 16., 7., -3.]]])
        np.testing.assert_array_equal(sys4.num, sys3.den)
        np.testing.assert_array_equal(sys4.den, sys3.num)
        
if __name__ == "__main__":
    unittest.main()