# shell learn

## shell type 

```
cat /etc/shells
```

查看系统支持的 shell.

```
grep tianya /etc/passwd
```

查看当前用户使用的 shell

## init shell
init shell 一般存在在 /etc/rc.d/init.d or /etc/init.d

## execute shell
syntax: 
bash your-script-name
sh your-script-name
./your-script-name

Examples:
$ bash bar
$ sh bar
$ ./bar

NOTE In the last syntax ./ means current directory, But only . (dot) means execute given command file in current shell without starting the new copy of shell, The syntax for . (dot) command is as follows
Syntax:
. command-name

Example:
$ . foo

## variables in shell
In Linux (Shell), there are two types of variable:
(1) System variables - Created and maintained by Linux itself. This type of variable defined in CAPITAL LETTERS.
(2) User defined variables (UDV) - Created and maintained by user. This type of variable defined in lower letters.

maybe you can use "$ set" command to query all variables 

## special parameters
Character	Definition
$*	Expands to the positional parameters, starting from one. When the expansion occurs within double quotes, it expands to a single word with the value of each parameter separated by the first character of the IFS special variable.
$@	Expands to the positional parameters, starting from one. When the expansion occurs within double quotes, each parameter expands to a separate word.
$#	Expands to the number of positional parameters in decimal.
$?	Expands to the exit status of the most recently executed foreground pipeline.
$-	A hyphen expands to the current option flags as specified upon invocation, by the set built-in command, or those set by the shell itself (such as the -i).
$$	Expands to the process ID of the shell.
$!	Expands to the process ID of the most recently executed background (asynchronous) command.
$0	Expands to the name of the shell or shell script.
$_	The underscore variable is set at shell startup and contains the absolute file name of the shell or script being executed as passed in the argument list. Subsequently, it expands to the last argument to the previous command, after expansion. It is also set to the full pathname of each command executed and placed in the environment exported to that command. When checking mail, this parameter holds the name of the mail file.

## shell arithmetic

Syntax:
expr op1 math-operator op2

Examples: 
$ expr 1 + 3
$ expr 2 - 1
$ expr 10 / 2
$ expr 20 % 3
$ expr 10 \* 3
$ echo `expr 6 + 3`

Note:
expr 20 %3 - Remainder read as 20 mod 3 and remainder is 2.
expr 10 \* 3 - Multiplication use \* and not * since its wild card.


## quotes
There are three types of quotes

| Quotes | Name          | Meaning
| "      | Double Quotes | "Double Quotes" - Anything enclose in double quotes removed meaning of that characters (except \ and $).
| '      | Single quotes | 'Single quotes' - Enclosed in single quotes remains unchanged.
| `      | Back quote    | `Back quote` - To execute command


## read statement
Syntax: 
read variable1, variable2,...variableN

Following script first ask user, name and then waits to enter name from the user via keyboard. Then user enters name from keyboard (after giving name you have to press ENTER key) and entered name through keyboard is stored (assigned) to variable fname.

```
$ vi sayH
#
#Script to read your name from key-board
#
echo "Your first name please:"
read fname
echo "Hello $fname, Lets be friend!"
```

## more commands on one command line 
Syntax:
command1;command2
To run two command with one command line.


## Linux Command Related with Process

Following tables most commonly used command(s) with process:

| For this purpose                                                  | Use this Command                  | Examples*
| To see currently running process                                  | ps                                | $ ps
| To stop any process by PID i.e. to kill process                   | kill    {PID}                     | $ kill  1012
| To stop processes by name i.e. to kill process                    | killall   {Process-name}          | $ killall httpd
| To get information about all running process                      | ps -ag                            | $ ps -ag
| To stop all process except your shell                             | kill 0                            | $ kill 0
| --                                                                | --                                | --
| For background processing                                         | linux-command  &                  | $ ls / -R 管道 wc -l &
| (With &, use to put particular command and program in background) |                                   |
| --                                                                | --                                | --
| To display the owner of                                           | ps aux                            | $ ps aux
| the processes along with the processes                            |                                   |
| --                                                                | --                                | --
| To see if a particular process is running or not.                 |                                   | For e.g. you want to see whether Apache web server process
| For this purpose you have to use ps command                       |                                   | is running or not then give command
| in combination with the grep command                              | ps ax grep  process-U-want-to see | $ ps ax 管道 grep httpd
| --                                                                | --                                | --
| To see currently running processes and other information          | top                               | $ top
| like memory and CPU usage with real time updates.                 |                                   |
| --                                                                | --                                | --
| To display a tree of processes                                    | pstree                            | $ pstree

## test command or [ expr ]
please see the page http://www.freeos.com/guides/lsst/ch03sec02.html   

## 摘录
source scriptName 在当前进程下执行 shells

bash -x scriptName debug shell

system wild configuration /etc/profile

