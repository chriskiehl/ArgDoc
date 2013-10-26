import argparse


def main():
	parser = argparse.ArgumentParser(description='Validates all HTML/CSS in projects folder(s)')
	parser.add_argument('-v','--ver', help="Set Doctype version to validate against")
	parser.add_argument('-a','--auto', help="Attempt to automatically detect Doctype", required=True)
	parser.add_argument('-o','--out', help='Save output to text file')
	parser.add_argument('-c','--css', help='Set check CSS to False', action='store_false')
	parser.add_argument('-m','--html', help='Set check HTML to False', action='store_false')
	parser.add_argument('-r', '--rec', help='Recursively walk through all folders in the project directory', required=True)
	parser.add_argument('-g','--verbose', help='Toggle verbose output on', action='store_true', required=True)
	parser.add_argument('-l','--highlight', help='Highlight reported errors in HTML files')
	parser.add_argument('filename', help='Filename(s) to validate')
	args = parser.parse_args()


if __name__ == '__main__':
	main()

