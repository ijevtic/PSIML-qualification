
# Problem statement

An old computer has a filesystem that can only contain files and directories.
The available terminal has only three commands (they start with $ in the input):

    ls lists the contents of the current dir in no particular order
    cd <dir> changes the current dir to <dir> (note that this is just a dir name, not a path)
        cd .. special notation changes the current dir to its parent
        cd / special notation changes the current dir to the root dir
    rm <file> removes a file

File and directory names are composed of alphanumeric characters, dots (.) and underscores (_). As output of ls command, all file names start with (f) (example: (f)file_name.ext) and directory names start with (d) (example: (d)dir_name.example) without whitespaces between (d)/(f) and its name. There cannot be multiple directories with the same name listed in one directory. There cannot be multiple files with the same name listed in one directory. Someone who wrote these commands may know where some directories are located and changed them without listing first. Directories cannot be named as .. as command cd .. would be ambiguous.

File and directory names are composed of alphanumeric characters, dots (.) and underscores (_). As output of ls command, all file names start with (f) (example: (f)file_name.ext) and directory names start with (d) (example: (d)dir_name.example) without whitespaces between (d)/(f) and its name. There cannot be multiple directories with the same name listed in one directory. There cannot be multiple files with the same name listed in one directory. Someone who wrote these commands may know where some directories are located and changed them without listing first. Directories cannot be named as .. as command cd .. would be ambiguous.
## Task 1: Find the number of files and directories.

    Print the total number of directories to the standard output
        Root directory should not be counted
    Print the total number of files to the standard output

## Task 2: Draw the sorted dir tree

    Given a list of commands and their outputs, print the dir tree to the standard output
    Directories come first, then files
    Both directories and files are sorted in the ascending order
    Unlisted directories should have ? printed at the end of it's content list to point out that we don't fully know it's content.
    Content of empty directory should be omitted.

Use one of the python built-in methods sorted() or sort() for sorting files and directories. Sorting example:

    Unsorted list: ['20', '1', '_1', '2', 'a1', '1_', '1a', '.1', 'A1', '1A', '1.', '10']
    Sorted list: ['.1', '1', '1.', '10', '1A', '1_', '1a', '2', '20', 'A1', '_1', 'a1']

## Task 3: Remove duplicated files

    Print to standard output a minimum list of commands that removes all but the first appearance (starting from top to bottom) of each duplicated file from the dir tree
    Avoid returning to root ($ cd /)
    Duplicated files should be deleted in the same order as printed in task 2
    Each command should be printed in a separate line
    Each command should be composed of $, operation (can be: cd or rm) and object (can be: .., <dirname/filename, /) separated by whitespace
    Start from the root dir ($ cd / command)
    Once the last duplicated file is deleted, task is completed

Data sets

There are two data sets:

    Public data set is used for developing your solution. After you submit your solution, you will be able to see how well your solution performs against this data set.
    Public data set is not used for calculating the final score.
    Private data set is used for testing your solution. The final score will be measured against this data set.
    Private data set and the final score will be available after the homework finishes.

## Input

Inputs are given through standard input

First line is always $ cd / . Each line of input represents a command (starts with $) or command output.
## Output

All results should be printed to the standard output. Results for each document should be printed in the following order:

    Solution of the 1st task:
        First line should be the number of directories
        Second line should be the number of files
    Solution of the 2nd task: Directory and file tree
        Depth level (counting from root) is represented by number of |- preceding file/directory name. Directories and files that are content of the root directory are considered to be in the first level.
        There should be no whitespaces between |- and file/directory name
        Printed directories should have / at the end of their name
        Unlisted directory should have ? printed at the end of their content list
        Empty directories should not have any content printed
    Solution of the 3rd task: Commands for removing duplicated files.
        Each command should be in a separate line.
        First command is always $ cd /.
        Last command should be the command that removes the last duplicated file
        If there are no duplicated files, output of this task should be omitted.

### Example
#### Input

```
$ cd /   
$ ls  
(f)file1 (d)dir1 (d)dir2 (f)file2   
$ cd dir1   
$ ls  
(f)file1   
$ cd ..   
$ cd dir2   
$ ls  
(d)dir3 (f)file3   
$ cd dir3   
$ ls  
(d)dir4 (f)file1 (d)dir5   
$ cd dir5   
$ ls    
```
#### Output
```
5  
5  
/  
|-dir1/  
|-|-file1  
|-dir2/  
|-|-dir3/  
|-|-|-dir4/  
|-|-|-|-?  
|-|-|-dir5/  
|-|-|-file1  
|-|-file3  
|-file1  
|-file2   
$ cd /   
$ cd dir2   
$ cd dir3   
$ rm file1   
$ cd /   
$ rm file1  
```
## Scoring

    Correct result for task 1 brings 4 points per test case.
    Correct result for task 2 brings 10 points per test case.
    Correct result for task 3 brings 6 points per test case.

Task 3 won't be evaluated if answers for task 1 and task 2 are not correct.
Constraints

    Time limit is 1s.
    Memory limit is 64 MB.
    Only standard libraries are allowed

If in doubt, please check announcements or refer to the data from the public data set and proceed with a reasonable assumption.
