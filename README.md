ArgDoc
======

<p align="center">
	<img src="https://raw.github.com/chriskiehl/ArgDoc/master/img/argdoc_main.png"/>
</p> 


What is it?
-----------

ArgDoc is a documentation generator (of the (hopefully) aesthetic variety) for command line programs. 

Features
-------- 

* Generate  documentation in `Markdown` or `HTML`.  
* Has detailed, ready-made instructions non-techie end-users. (enable with the `noob` flag). 

ArgDoc came to be when I started freelancing building one-off scripts for clients. The documentation needed to be gentle, friendly, non-ugly, and above all else non-techie freindly. So, with those needs in mind, I added an option for including detailed instructions on the basic "how to" of command line programs. It answers questions such as "what is a flag," and "How do I run this." Basic stuff to get someone unfamiliar with the command line up and running. 

Requirements 
----------
* [argparse](http://docs.python.org/dev/library/argparse.html)

ArgDoc works by parsing the Python AST and pulling out references to `argparse.ArgumentParser`, so the older [optparse](http://docs.python.org/2/library/optparse.html) module will not work (though support could be wrangled in if anyone needs it).   


---  


Usage
-----

ArgDoc comes in three flavors; all of them named `generate_doc`

* `@generate_doc` *( decorator )*  
* `generate_doc()` *( function )*
* `generate_doc`  *( commandline )*   
 

####@generate_doc

Suggested method. Simply decorate your main function with `@generate_doc` and everytime you run your program up-to-date documentation will be generated. 

To run with default settings: 

    @generate_doc 
    def main():
        parser = argparse.ArgumentParser(bla bla bla) 
        # rest of code.. 
        
    
or with settings of your choice. 

    @generate_doc(format='pdf', beginner=True)
    def main():
        parser = argparse.ArgumentParser(bla bla bla) 
        # rest of code.. 

####generate_doc()

Alternatively, you can pass your `ArgumentParser` object to the `generate_doc` function directly. 

    from argdoc import generate_doc 
    
    def main(): 
        parser = argparse.ArgumentParser(whatevs) 
        parser.add_argument() 
        ... 
        
        generate_doc(parser)


####generate_doc (commandline) 

Finally, if preferred, you can run argDoc as a commandline tool. 

    $user python argdoc.py --f pdf name_of_script_to_document.py   

----  


Contact
-------
Feature request? Bug? Hate it?  
Drop me a line at audionautic@gmail.com

-----------------------------------------------------------  

--------------------------------------------------------------  


###Sample Output 

Below is a sample output for a HTML/CSS validator tool. It has the noob instructions enabled so you can get a feel for what the whole document looks like. 

test_input.py 
==============  
Validates all HTML/CSS in projects folder(s)  

---   
How To Use
-------------  

Command line programs have three main parts:  

1. Program Name
2. Flags (optional)
3. Arguments   



**Program Name**  
Simply the name of the program you want to run.    

     $ python test_input.py

**Flags**  
Flags are completely optional. They can be used to modify the way the program is run. For instance, to change where an output file is saved. They are preceded by two dashes and the name of the flag. 

    --outfile  myfilename.txt
    
Flags can also be set via a shortened form which consists of a single dash, and (commonly) the first letter of the flag name.   

    -o myfilename.txt
    
**Arguments**  
If required by the program, arguments are used to give information that the program needs to do its work. For instance, in a calculator application, Arguments would be the numbers and operators that you give to the program to calculate

    $ calc.exe 5 + 2  
    
**Example**  

Using all of the above info, here is an example of running a command line program with both flags and arguments. 

    $ python calc.py --saveresults myfile.txt 38 / 2 
    

Documentation
-------------     
  
| Option String | Required | Choices | Default| Option Summary |  
|---------------|----------|---------|--------|----------------|  
| ['-h', '--help'] | False | None | ==SUPPRESS== | show this help message and exit | 
| ['-v', '--ver'] | False | None | None | Set Doctype version to validate against | 
| ['-a', '--auto'] | True | None | None | Attempt to automatically detect Doctype | 
| ['-o', '--out'] | False | None | None | Save output to text file | 
| ['-c', '--css'] | False | None | True | Set check CSS to False | 
| ['-m', '--html'] | False | None | True | Set check HTML to False | 
| ['-r', '--rec'] | True | None | None | Recursively walk through all folders in the project directory | 
| ['-g', '--verbose'] | True | None | False | Toggle verbose output on | 
| ['-l', '--highlight'] | False | None | None | Highlight reported errors in HTML files | 
| [] | True | None | None | Filename(s) to validate |   
		











