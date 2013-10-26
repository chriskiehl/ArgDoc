{module_title} 
==============  
{prog_decription}  

---   
How To Use
-------------  

Command line programs have three main parts:  

1. Program Name
2. Flags (optional)
3. Arguments   



**Program Name**  
Simply the name of the program you want to run.    

     $ python {module_title}

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
{table_data}  
		
