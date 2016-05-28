# sed learn

## introduciton
How to use sed, a special editor for modifying files automatically. If you want to write a program to make changes in a file, sed is the tool to use.


## s for substitution
A simple example is changing "day" in the "old" file to "night" in the "new" file:

```
sed 's/day/night/' <old >new
```

Or another way (for UNIX beginners),

```
sed 's/day/night/' old >new
```

and for those who want to test this:

```
echo day | sed 's/day/night/' 
```

This will output "night".


Another important concept is that sed is line oriented. Suppose you have the input file:

one two three, one two three
four three two one
one hundred
and you used the command

sed 's/one/ONE/' file 

The output would be

ONE two three, one two three
four three two ONE
ONE hundred

Note that this changed "one" to "ONE" once on each line


