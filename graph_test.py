import unittest

from breadboard.graph import BreadGraph


class GraphTest(unittest.TestCase):

    def test_or_TT(self):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', True)
        graph.add_node(0, 0, 'input2', 'transmit', True)

        graph.add_node(0, 0, 'or', 'OR')

        graph.add_edge('input1', 'or')
        graph.add_edge('input2', 'or')

        result = graph.calculate()

        self.assertEqual(list(result.values())[0], True)

    def test_or_TF(self):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', True)
        graph.add_node(0, 0, 'input2', 'transmit', False)

        graph.add_node(0, 0, 'or', 'OR')

        graph.add_edge('input1', 'or')
        graph.add_edge('input2', 'or')

        result = graph.calculate()

        self.assertEqual(list(result.values())[0], True)

    def test_or_FF(self):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', False)
        graph.add_node(0, 0, 'input2', 'transmit', False)

        graph.add_node(0, 0, 'or', 'OR')

        graph.add_edge('input1', 'or')
        graph.add_edge('input2', 'or')

        result = graph.calculate()

        self.assertEqual(list(result.values())[0], False)

    def test_half_adder_TT(self):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', True)
        graph.add_node(0, 0, 'input2', 'transmit', True)

        graph.add_node(0, 0, 'xor', 'XOR')
        graph.add_node(0, 0, 'and', 'AND')

        graph.add_edge('input1', 'xor')
        graph.add_edge('input1', 'and')

        graph.add_edge('input2', 'xor')
        graph.add_edge('input2', 'and')

        result = graph.calculate()

        self.assertEqual(result['xor'], False)
        self.assertEqual(result['and'], True)

    def test_half_adder_FF(self):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', False)
        graph.add_node(0, 0, 'input2', 'transmit', False)

        graph.add_node(0, 0, 'xor', 'XOR')
        graph.add_node(0, 0, 'and', 'AND')

        graph.add_edge('input1', 'xor')
        graph.add_edge('input1', 'and')

        graph.add_edge('input2', 'xor')
        graph.add_edge('input2', 'and')

        result = graph.calculate()

        self.assertEqual(result['xor'], False)
        self.assertEqual(result['and'], False)

    def test_half_adder_TF(self):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', True)
        graph.add_node(0, 0, 'input2', 'transmit', False)

        graph.add_node(0, 0, 'xor', 'XOR')
        graph.add_node(0, 0, 'and', 'AND')

        graph.add_edge('input1', 'xor')
        graph.add_edge('input1', 'and')

        graph.add_edge('input2', 'xor')
        graph.add_edge('input2', 'and')

        result = graph.calculate()

        self.assertEqual(result['xor'], True)
        self.assertEqual(result['and'], False)

    def build_full_adder_NAND(self, input1, input2, carry):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', input1)
        graph.add_node(0, 0, 'input2', 'transmit', input2)
        graph.add_node(0, 0, 'carry', 'transmit', carry)

        graph.add_node(0, 0, 'u1', 'NAND')
        graph.add_node(0, 0, 'u2', 'NAND')
        graph.add_node(0, 0, 'u3', 'NAND')
        graph.add_node(0, 0, 'u4', 'NAND')
        graph.add_node(0, 0, 'u5', 'NAND')
        graph.add_node(0, 0, 'u6', 'NAND')
        graph.add_node(0, 0, 'u7', 'NAND')
        graph.add_node(0, 0, 'u8', 'NAND')
        graph.add_node(0, 0, 'u9', 'NAND')

        graph.add_edge('input1', 'u1')
        graph.add_edge('input2', 'u1')

        graph.add_edge('input1', 'u2')
        graph.add_edge('u1', 'u2')

        graph.add_edge('input2', 'u3')
        graph.add_edge('u1', 'u3')

        graph.add_edge('u2', 'u4')
        graph.add_edge('u3', 'u4')

        graph.add_edge('u4', 'u5')
        graph.add_edge('carry', 'u5')

        graph.add_edge('u4', 'u6')
        graph.add_edge('u5', 'u6')

        graph.add_edge('u5', 'u7')
        graph.add_edge('carry', 'u7')

        graph.add_edge('u6', 'u8')
        graph.add_edge('u7', 'u8')

        graph.add_edge('u5', 'u9')
        graph.add_edge('u1', 'u9')

        return graph

    def test_full_adder_NAND_TTT(self):
        graph = self.build_full_adder_NAND(True, True, True)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertTrue(result['u8'])
        self.assertTrue(result['u9'])

    def test_full_adder_NAND_TTF(self):
        graph = self.build_full_adder_NAND(True, True, False)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertFalse(result['u8'])
        self.assertTrue(result['u9'])

    def test_full_adder_NAND_TFT(self):
        graph = self.build_full_adder_NAND(True, False, True)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertFalse(result['u8'])
        self.assertTrue(result['u9'])

    def test_full_adder_NAND_TFF(self):
        graph = self.build_full_adder_NAND(True, False, False)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertTrue(result['u8'])
        self.assertFalse(result['u9'])

    def test_full_adder_NAND_FTT(self):
        graph = self.build_full_adder_NAND(False, True, True)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertFalse(result['u8'])
        self.assertTrue(result['u9'])

    def test_full_adder_NAND_FTF(self):
        graph = self.build_full_adder_NAND(False, True, False)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertTrue(result['u8'])
        self.assertFalse(result['u9'])

    def test_full_adder_NAND_FFT(self):
        graph = self.build_full_adder_NAND(False, False, True)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertTrue(result['u8'])
        self.assertFalse(result['u9'])

    def test_full_adder_NAND_FFF(self):
        graph = self.build_full_adder_NAND(False, False, False)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertFalse(result['u8'])
        self.assertFalse(result['u9'])

    def build_full_adder_general(self, input1, input2, carry):
        graph = BreadGraph()

        graph.add_node(0, 0, 'input1', 'transmit', input1)
        graph.add_node(0, 0, 'input2', 'transmit', input2)
        graph.add_node(0, 0, 'carry', 'transmit', carry)

        graph.add_node(0, 0, 'xor1', 'XOR')
        graph.add_node(0, 0, 'xor2', 'XOR')

        graph.add_node(0, 0, 'and1', 'AND')
        graph.add_node(0, 0, 'and2', 'AND')

        graph.add_node(0, 0, 'or', 'OR')

        graph.add_edge('input1', 'xor1')
        graph.add_edge('input2', 'xor1')

        graph.add_edge('xor1', 'xor2')
        graph.add_edge('carry', 'xor2')

        graph.add_edge('xor1', 'and1')
        graph.add_edge('carry', 'and1')

        graph.add_edge('input1', 'and2')
        graph.add_edge('input2', 'and2')

        graph.add_edge('and1', 'or')
        graph.add_edge('and2', 'or')

        return graph

    def test_full_adder_general_TTT(self):
        graph = self.build_full_adder_general(True, True, True)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertEqual(result['xor2'], True)
        self.assertEqual(result['or'], True)

    def test_full_adder_general_TTF(self):
        graph = self.build_full_adder_general(True, True, False)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertEqual(result['xor2'], False)
        self.assertEqual(result['or'], True)

    def test_full_adder_general_TFT(self):
        graph = self.build_full_adder_general(True, False, True)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertEqual(result['xor2'], False)
        self.assertEqual(result['or'], True)

    def test_full_adder_general_TFF(self):
        graph = self.build_full_adder_general(True, False, False)

        result = graph.calculate()

        self.assertEqual(len(result.keys()), 2)
        self.assertEqual(result['xor2'], True)
        self.assertEqual(result['or'], False)


if __name__ == '__main__':
    unittest.main()
