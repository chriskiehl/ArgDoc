import os
import hashlib 
import unittest 
import sys
sys.path.insert(0, '..')
import makedoc


class TestArgDocParser(unittest.TestCase):
	def setUp(self): 
		f_html = self.load_file(os.path.join('expected_results', 'full.html')) 
		b_html = self.load_file(os.path.join('expected_results', 'basic.html')) 
		f_md = self.load_file(os.path.join('expected_results', 'full.md')) 
		b_md = self.load_file(os.path.join('expected_results', 'basic.md')) 

		self.full_html = hashlib.md5(f_html).hexdigest()
		self.basic_html = hashlib.md5(b_html).hexdigest()
		self.full_md = hashlib.md5(f_md).hexdigest()
		self.basic_md = hashlib.md5(b_md).hexdigest()


	def test_arg_to_full_html(self):
		'''Generate and test full html doc'''
		self._test('html', 1, filename='test_input.py_doc.html', test_against=self.full_html)

	def test_arg_to_basic_html(self):
		'''Generate and test basic html doc'''
		self._test('html', 0, filename='test_input.py_doc.html', test_against=self.basic_html)

	def test_arg_to_full_md(self): 
		'''Generate and test full markdown doc'''
		self._test('md', 1, filename='test_input.py_doc.md', test_against=self.full_md)

	def test_arg_to_basic_md(self): 
		'''Generate and test basic markdown doc'''
		self._test('md', 0, filename='test_input.py_doc.md', test_against=self.basic_md)


	def _test(self, *args, **kwargs):
		makedoc.parse_pyfile('test_input.py', *args)
		result = self.load_file(os.path.join(os.getcwd(), 'Docs', kwargs['filename']))
		
		self.assertEquals(kwargs['test_against'], hashlib.md5(result).hexdigest()) 


	# def _contruct_decorated_main(format, beginner):
	# 	with open('test_input.py', 'rb') as f:


	def load_file(self, filepath):
		with open(filepath, 'rb') as f:
			return f.read() 



# a = hashlib.md5(file_a).hexdigest()
# b = hashlib.md5(file_b).hexdigest()

# print a
# print b

if __name__ == '__main__':
	unittest.main()

	# with open('test_input.py', 'rb') as f:
	# 	data = [i for i in f.readlines()]
	# data[1] = '@ar'
	# for i in data: 
	# 	print i 
