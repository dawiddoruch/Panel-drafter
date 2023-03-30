I wrote this script to automate process of drafting ACM panels. 

Previously it took multiple hours to make drawings for dozens of ACM panels.
The whole process was tedious and thus prone to errors. The more time I've
spent making drawings the more frustrated I was and more errors were made and
I was not aware of them untill it came time to nest all the panels on ACM sheets.

Script takes in XLS spreadsheet with list of panels, dimensions and few other
attributes and generates separate DXF file for each one.

I am using nesting software to nest all the panels onto ACM sheets and then
run "Toolpath creator" script to generate g-code for Onsrud CNC router.
