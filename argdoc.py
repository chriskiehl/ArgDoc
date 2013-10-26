'''

Note: below code is 100 percent trial and error. I have no idea how 
ast is actually supposed to be used. I brute forced this one with the 
dir() function and a lot of patience.

Proceed with caution. 

The basic idea is to 

	a. find the index of the Argparse.ArgumentParser assignment in the code
	b. find the index of the parse_args() call 
	c. Get the name of the instance variable to which ArgumentParser was assigned
	d. Use that knowledge to extract all of the add_argument calls inbetween the 
		 index of the contructor, and the index of the parse_args() call. 

We'll see how robust this turns out to be.

'''


import os 
import ast 
import sys
import parser 
import random
import codegen
import argparse
from itertools import chain


class ParserError(Exception):
	'''Thrown when the parser can't find argparse functions the client code'''
	pass

def parse_argparse_statements(file_name):
	'''
	Parses the AST of the passed in Python file and extracts 
	all code that sets up the ArgumentParser class
	'''

	def find_main(nodes):
		for node in nodes.body: 
			if isinstance(node, ast.FunctionDef) and node.name == 'main':
				return node
		raise ParserError('Could not find `def main()`')

	def is_func(x, func_name):
		try: return x.value.func.attr == func_name
		except: return False # Wrong type. Contine. 

	def get_assignment_name(node): 
		return node.targets[0].id 

	def get_help_desc(node): 
		return node.value.keywords[0].value.s

	nodes = ast.parse(open(os.path.abspath(file_name)).read())

	mainfunc = find_main(nodes)
	
	nodes = [node for node in mainfunc.body
		if is_func(node, 'add_argument')
		]
	# get the main ArgumentParser assignment
	argparse_assign_obj = filter(
		lambda x: is_func(x, 'ArgumentParser'), mainfunc.body)[0]

	parser_var_name = get_assignment_name(argparse_assign_obj)
	prog_description = get_help_desc(argparse_assign_obj)
	ast_source = list(chain([argparse_assign_obj], nodes))

	# convert ast to python code
	code = map(codegen.to_source, ast_source)
	# Add line of code which stores the argparse values
	code.append('INFO = {}._actions'.format(parser_var_name))

	return {
		'code': code, 
		'parser_variable_name' : parser_var_name,
		'description' : prog_description
	}

def parse_pyfile(file_name, format='html', beginner=1, success_msg=1):
	print 'parse_pyfile file_name:', file_name
	py_source = parse_argparse_statements(file_name)

	client_arg_info = extract_values_from_code(py_source['code'])
	output = markup(file_name, py_source['description'], client_arg_info, format=format, beginner=beginner)

	outfile_name = '{name}_doc.{ext}'.format(name=file_name, ext=format)
	save_doc(outfile_name, output)

	if success_msg:
		print 'Sucess!'
		print 'Saved documentation to /Docs/{}'.format(outfile_name)


def markup(title, description, arg_info, format, beginner):
	'''
	Loads the appropriate template based on the format argument and
	renders it with the dict content stored in the arg_info list.   
	'''
	def _open(filename):
		base_dir = os.path.join(os.path.split(os.path.abspath(__file__))[:-1])[0]
		file_path = os.path.join(base_dir, 'templates', filename)
		with open(file_path) as f: 
			return f.read()
		
	def load_template(): 
		if not beginner:
			return _open('basic.' + format)
		return _open('full.' + format)

	def render(**kwargs):
		template = load_template()
		return template.format(**kwargs)

	def build_table(arg_info):
		table_output = []
		if format == 'md': 
			row = '| {option_strings} | {required} | {choices} | {default} | {help} | '
		else: 
			row = ''.join(
				['<tr><td>{option_strings}</td><td>{required}</td>',
				'<td>{choices}</td><td>{default}</td><td>{help}</td></tr>']
				)

		for attribs in arg_info:
			table_output.append(row.format(
						option_strings=vars(attribs)['option_strings'],
						required=vars(attribs)['required'],
						choices=vars(attribs)['choices'],
						default=vars(attribs)['default'],
						help=vars(attribs)['help']
						))
		return '\n'.join(table_output)

	output = render(module_title=os.path.split(title)[-1],
		prog_decription=description,
		table_data=build_table(arg_info))

	# Stupid work around for the css in html
	# I couldn't store curly brackets, as it fudges
	# up the string formatting. So curly braces are 
	# marked up as [% and %] 
	if format == 'html':
		output = output.replace('[%', '{')
		output = output.replace('%]', '}')

	return output
	
def save_doc(filename, output):
	def mkdir(foldername):
		if not os.path.isdir(os.path.join(os.getcwd(), foldername)):
			try: 
				os.mkdir('Docs')
			except WindowsError:
				raise WindowsError("Could not create Docs directory")

	base_dir, file_name = os.path.split(filename)

	foldername = 'Docs'
	mkdir(foldername)

	with open(os.path.join(base_dir, foldername, file_name), 'wb') as f: 
		f.write(output)

def make_random_filename(length):
	filename = 'tmp_' + ''.join([str(random.randint(0,10)) for _ in range(length)]) + '.py'
	# Make sure it doesn't inadvertently write over a 
	# file (as slim of a chance as that may be)
	while os.path.exists(os.path.join(os.getcwd(), filename)):
		make_random_filename()
	return filename


def	extract_values_from_code(code):
	'''
	extracts the _actions attribute from the client
	source file by: 

		a. Saving code to a temporary python file.
		b. Importing the file as a module
		c. Grabing its stored values
		d. Deleting the python file.

	returns the attributes of the module.  
	'''
	def save_to_module():
		try: 
			with open(tmp_file, 'wb') as f:
				f.write('import argparse\n')
				for line in code: 
					f.write('{}\n'.format(line))
		except IOError:
			raise IOError('Could not save temporary file')

	def load_module():
		module_name, _ = os.path.splitext(tmp_file)
		return __import__(module_name)
	
	def delete_module():
		try: 
			os.remove(tmp_file)
			os.remove(tmp_file.replace('.py', '.pyc'))
		except Exception:
			print 'WARNING: Failed to delete temporary file {}.'.format(tmp_file)

	try:
		tmp_file = make_random_filename(20)
		save_to_module()
		module = load_module()
		return module.INFO

	finally:
		delete_module()	

def test_run():
	'''
	Runs a simple test file to make sure things 
	haven't horrifically broken
	'''
	parse_pyfile('test_input.py')


def build_doc_from_parser_obj(file_name, parser_obj, format='html', beginner=1, success_msg=1):
	prog_description = parser_obj.description
	client_arg_info = parser_obj._actions

	output = markup(file_name, prog_description, 
		client_arg_info, format=format, beginner=beginner)

	outfile_name = '{name}_doc.{ext}'.format(name=file_name, ext=format)
	# print 'outfile_name', outfile_name
	# print 'file_name', file_name
	save_doc(outfile_name, output)

	if success_msg: 
		print 'Sucess!'
		print 'Saved documentation to /Docs/{}'.format(os.path.split(outfile_name)[-1])


def generate_doc(f=None, format='html', beginner=1, success_msg=1):

	'''
	Decorator for client code's main function. 
	It gets the name of the calling script, loads it 
	into parse_pyfile(), and generates the documentation, 
	before finally calling the main() function to resume 
	execution as normal. 
	'''

	# Handles if the passed in object is instance 
	# of ArgumentParser. If so, it's being called as 
	# a function, rather than a decorator
	if isinstance(f, argparse.ArgumentParser):
		filename = sys.argv[0]

		build_doc_from_parser_obj(
			file_name=filename, 
			parser_obj=f, 
			format=format, 
			beginner=beginner, 
			success_msg=success_msg
			)
		return 

	# --------------------------------- #
	# Below code is all decorator stuff #
	# --------------------------------- #
	def get_caller_path():
		# utility func for decorator
		# gets the name of the calling script
		tmp_sys = __import__('sys')
		return tmp_sys.argv[0]

	def generate_docs(f):
		def inner():
			module_path = get_caller_path()
			path = os.path.join(*os.path.split(module_path)[:-1])
			filename = '{}'.format(os.path.split(module_path)[-1])
			parse_pyfile(filename, format=format, beginner=beginner, success_msg=success_msg)
		inner.__name__ = f.__name__ 
		return inner

	if callable(f):
		return generate_docs(f)
	return generate_docs




# @generate_doc
def main():
	parser = argparse.ArgumentParser(
		description='argdoc turns all argparse arguments into beautiful, end-user friendly documentation',
		formatter_class=argparse.RawTextHelpFormatter)
	
	parser.add_argument(
		'filename', 
		help="Name of the file for which you want to create documentation")
	
	parser.add_argument(
		'-f', '--format', 
		help="Format of the outputted documentation.\nOptions: ['md', 'html']" + 
			"\nDefault: 'html'",
		choices=['md', 'html'],
		default="html",
		metavar="")

	parser.add_argument(
		'-n', '--noob', 
		help=("Set whether or not to include the beginner instructions in the Docs"
			'\n(See templates for example of beginner info.)'),
		action="store_false", 
		default=True)

	parser.add_argument(
		'-q', '--quiet',
		help="Supresses success message",
		action='store_false')

	args = parser.parse_args()
	parse_pyfile(args.filename, format=args.format, beginner=args.noob)


if __name__ == '__main__':
	main()

