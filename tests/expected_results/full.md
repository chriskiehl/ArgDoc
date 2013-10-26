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
		
