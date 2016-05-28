# shell struct

## if ... else ... fi
Syntax:

           if condition
           then
                       condition is zero (true - 0)
                       execute all commands up to else statement

           else
                       if condition is not true then
                       execute all commands up to fi
           fi


## multilevel if - then - else
Syntax:
           if condition
           then
                       condition is zero (true - 0)
                       execute all commands up to elif statement
           elif condition1 
           then
                       condition1 is zero (true - 0)
                       execute all commands up to elif statement  
           elif condition2
           then
                       condition2 is zero (true - 0)
                       execute all commands up to elif statement          
           else
                       None of the above condtion,condtion1,condtion2 are true (i.e. 
                       all of the above nonzero or false)
                       execute all commands up to fi
           fi

## Loops in shell
Bash supports:

	for loop
	while loop

### for loop
Syntax:
            for { variable name } in { list }
            do
                     execute one for each item in the list until the list is
                     not finished (And repeat all statement between do and done)
            done


### while loop
Syntax:

           while [ condition ]
           do
                 command1
                 command2
                 command3
                 ..
                 ....
            done

## case statement
Syntax:
           case  $variable-name  in
                pattern1)   command
                                ...
                                ..
                                command;;
                pattern2)   command
                                ...
                                ..
                                command;;
                patternN)   command
                                ...
                                ..
                                command;;
                *)             command
                                ...
                                ..
                                command;;
           esac

## debug shell
Syntax:
sh   option   { shell-script-name }
OR
bash   option   { shell-script-name }
Option can be
-v Print shell input lines as they are read.
-x After expanding each simple-command, bash displays the expanded value of PS4 system variable, followed by the command and its expanded arguments.
