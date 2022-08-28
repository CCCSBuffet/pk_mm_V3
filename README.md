# Chair / Dean Tool Version 3

## Summary

This is a Python 3 command line tool that processes reports generated
each month currently by Mike Jonas and sent to Chairs and Deans. The
report sent to Chairs contains only select Majors and Minors. The report
sent to Deans contains all Majors and Minors within their Division. This
tool works equally well on either file format.

The purpose of the tool is to:

- provide reports containing historical context

- provide reports for a specific month

Several of the reports can produce output in both text and graph form.

The reports can be useful for:

- Identifying trends in a Major's size over time or in a specific month

- Knowing the size of each cohort within a Major over time or in a
specific month or in a specific term

- Generating email lists from a particular month optionally limited by
cohort and by GPA. For example:

  - Who were my Seniors in April 2019

  - Which current students have a GPA <= 2.0

- Identifying frequent double Majors

- Identifying

Textual reports can be emitted with headers or without and can also be
imported into Excel.

## About

The tools described herein were created by Prof. Perry Kivolowitz of
the Computer Science Department.

## The Data

Each month, a report arrives via email. The report comes in the form of
a compressed Excel spreadsheet (i.e. one with a file name ending in
".xlsx"). This file must be loaded into Excel and exported in one or
two ways.

The Excel spreadsheet always arrives with the same name and never
contains any indication of what month to which it corresponds.

At a minimum, use Excel to rename the file for export as a CSV file.

File names must follow this standard:

```text
MM-YYYY-mm.csv
```

Where:

| Symbol | Meaning |
| ------ | ------- |
| MM | This is a literal string |
| YYYY | Four digit year |
| mm | Two digit month |
| .csv | This a literal string |

Please note that if you have files from 2017 or earlier, they have not
been tested.

<div class="page"/>

A best practice for file handling is to accumulate all of your CSV
files into a single folder (directory). We suggest a folder that is
easy to navigate to via text. For example, on a Mac you can place
the CSV folder in your Documents directory if you so choose. Assuming
that you have named your folder "csv", you will refer to the folder on
the command line as "~/Documents/csv".

We further suggest saving the original Excel file in a different folder
having first been named properly.

## Installation

### (Modern) Windows

Get Python if you do not already have it. You can determine if you
already have python by opening a command prompt and typing:
`python --version`

If you see a response from python listing a version at 3 or above, you
are set and do not have to install python.

To install python:

- Open the Microsoft Store

- Click the tile indicating the Python with the latest version 3 that
is not marked as "(RC)"

- Click "Install"

- Close the Microsoft Store

You can now confirm you have python by performing the step described
above.

To install matplotlib:

- Open a command prompt

- Enter `pip install matplotlib` and hit return. A lot of output should
follow with the word "Successfully" near the bottom of the output.

To get the tool:

This is not defined yet. Contact pkivolowitz@carthage.edu.

Helpful Windows tip:

For the commands that generate pictures, the picture can be opened
directly from the command prompt by typing its name and hitting enter.

### On Macintosh

The Mac comes out of the box with python! Great! Actually not so great.

Apple thoughtfully includes python 2. This tool is written for python
3. Both python 2 and 3 are current versions and they are incompatible.

Still more amazingly, installing python 3 is not that easy. Why? Apple.

Follow the directions on this
[web page](https://macappstore.org/python3-2/).

After installing python 3, confirm its presence by entering
`python3 --version`. Note the `3`.

Assuming you have `python3`, you will also have `pip3`. Enter
`pip3 install matplotlib` in the terminal.

To get the tool:

This is not defined yet. Contact pkivolowitz@carthage.edu.

## The Command Line

### On Windows

Enter the command line by typing the Windows key along with the R key
(un-shifted). It will open in your home directory. You must navigate
to where you installed the tool. This is done with the cd command.

Suppose you installed the tool in Documents\chair_tool, you would:
`cd Documents\chair_tool`.

### On Macintosh

Enter the terminal application. This is easily done using Spotlight
Search. It will open in your home directory. You must navigate to
where you installed the tool. This is done with the cd command.

Suppose you installed the tool in Documents/chair_tool, you would:
`cd ~/Documents/chair_tool`.

## Running the Tool

### On Windows

The beginning of the command you must enter is: `python main.py`.

### On Macintosh

The beginning of the command you must enter is: `python3 main.py`.

## Specifying Required Options

The action of the tool is determined by the options specified on the
command line.

Options are indicated by words following `--`. In this next example,
the "folder" and "major" are required:

```text
python3 main.py --folder ~/Documents/csv --major "Computer Science"
```

the preceding is for the Mac. For Windows it might look like this:

```text
python main.py --folder %USERPROFILE%\Documents\csv --major "Computer Science"
```

Isn't that pleasant?

The `--folder` along with a path to your data is required. Note that if
you administer multiple programs and get separate spreadsheets for each,
segregate the files into different directories and then use the
`--folder` argument to differentiate between them.

If your Major's formal name contains a space, you must surround the
name with double quotes. So, Biology can be specified with
`--major Biology` but Data Science must be specified with
`--major "Data Science"`.

## Specifying Modifier Options

Some of the defined options modify other options.

### `start_month`

Several reports are sensitive to the `start_month` modifier. Specifying
it causes collected data to begin with the named file. If missing, the
starting month is set to the earliest file you have.

Suppose you have files going back to 2019. You can specify a report
to start with April 2019 by using: `--start_month MM-2019-04`.

### `end_month`

Several reports are sensitive to the `end_month` modifier. Specifying
it causes collected data to end with the named file. If missing, the
ending month is set to the latest file you have.

Some reports work with one month only (`--gpa` for example). You
specify the month using `--end_month`.

### `gpa_le`

This modifier works only with `--gpa` and `--email`. In all respects
`--email` is a synonym for `--gpa`. If you specify the `--gpa_le`
modifier, you follow it with a number representing the *maximum* GPA
to consider. If you leave this modifier out, then all GPAs will be
considered.

Suppose you wanted to email current Sophomores with a GPA less than or
equal to 2.5. Your command line might be:

```text
python3 main.py --folder csv --major "Computer Science" --gpa SO --gpa_le 2.5
```

### `graph`

If the report you want can also produce a graph in addition to a textual
report, specifying `--graph` switches the output to graphical.

For example `--counts` produces text. `--counts --graph` produces a
picture.

### `term`

Some reports are aware of terms in addition to months. Specifying
`--breakdown` produces the breakdown report for all months.
Specifying `--breakdown --term fall` produces the breakdown report
from all Fall terms. Note that covering several months in a term
causes some supported reports to average the results of the months
that comprise the term.

### `quiet`

For textual reports, specifying `--quiet` causes the report to
lack its headings. This might make import into Excel easier.

## Error Handling

There are two kinds of text output (in common between Windows,
Mac and Linux and many other operating systems). These are

- stdout - where normal text goes and

- stderr - where error text can go

The benefit of this is that normal and error output can be
split to go to do different destination. By default they
go to the same place.

For example:

```text
python3 main.py --folder csv --major "Computer Science" --breakdown --start_month MM-2018-01 --end_month MM-2018-12
```

produces the following for Computer Science:

```text
2018 6 was missing
2018 7 was missing
2018 11 was missing
Year Term         FF     SO     JR     SR
2018 j-term       27      8     21     19
2018 spring       28      9     20     20
2018 summer       38     20      9     24
2018 fall         33     19      9     24
```

Notice Computer Science is missing June, July and November of 2018.
These missing months are printed to `stderr`. If you need only the
normal output, you can send the error text someplace else.

On Windows, here is how you would send errors to the bit bucket

```text
python main.py --folder csv --major "Computer Science" --breakdown --start_month MM-2018-01 --end_month MM-2018-12 2> NUL
Year Term         FF     SO     JR     SR
2018 j-term       27      8     21     19
2018 spring       28      9     20     20
2018 summer       38     20      9     24
2018 fall         33     19      9     24
```

On the Mac, here is the same thing:

```text
python3 main.py --folder csv --major "Computer Science" --breakdown --start_month MM-2018-01 --end_month MM-2018-12 2> /dev/null
Year Term         FF     SO     JR     SR 
2018 j-term       27      8     21     19
2018 spring       28      9     20     20
2018 summer       38     20      9     24
2018 fall         33     19      9     24
```

## The Reports - High Level

### `--gpa` and `--email`

These are synonyms. They produce a customizable textual report containing
certain student information.

For example:

```text
python3 main.py --folder csv --major "Computer Science" --gpa SO --end_month MM-2020-01 2> /dev/null
Sophomores
ID      Last Name       First Name      Gender  GPA     Email           
NNNNNN  x               x               F       3.9     x x <xx@carthage.
MMMMMM  y               y               M       3.66    y y <yy@carthage.edu>
PPPPPP  z               z               M       2.125   z z <zz@carthage.edu>
--snip--
```

This command gets the email addresses, genders, student IDs and GPAs of
just the Sophomores in Computer Science in January 2020.

Note the format of the email addresses. These are expanded format
addresses which list both the real name and the email address of each
person.

`--graph` is not honored.

`--term` is not honored.

`--gpa_le` is honored.

Usage examples:

- Who were your majors in a certain month in the past?

- What Juniors were in GPA jeopardy?

- Which Seniors have GPAs above 3.5 and should be listed for Departmental
honors?

- Which Juniors might serve as tutors?

### `--counts`

### `--breakdown`

### `--Pairings` and `--pairings`

