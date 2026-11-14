# Docchat (with file reading and calculating abilities)
This project allows you to run ChatGPT by Open-AI and call the tools: calculate, ls, cat and grep, which allow evaluate mathematical expressions, list the files in a folder, read a file, and search for patterns in a file, respecitively.

Calling ls through chat in test_projects/discoveries_in_the_tidepools:

``` bash
$ cd test_projects/discoveries_in_the_tidepools
$ chat
chat> ls
Here are the files in the current directory:

- README.md
- bat_star.png
- index.html
- index2.html
- index3.html
- monterey_dorid.png
- red_abalone.png
- style.css
- thatsme.png
- tidepoolingSafety.png
chat> Which files are named for sea creatures?
**Sea‑creature‑named files**

- `bat_star.png`  – a bat‑star (starfish)  
- `monterey_dorid.png` – a Monterey dorid sea slug  
- `red_abalone.png` – a red abalone  

These are the files whose names refer to marine animals.
chat>
```
This example shows that ls without an argument returns all the files in the current folder. It also shows how the chat bot can "remember" and work with previous results.


Calling grep manually in test_projects/ebay-scraper.

``` bash
$ cd test_projects/ebay-scraper
$ chat
chat> \grep "Used planter 1" *.json
garden tools.json:    "name": "Used planter 1",
garden tools.json:    "name": "Used planter 10",
poster.json:    "name": "Used planter 1",
poster.json:    "name": "Used planter 10",
stuffed animal.json:    "name": "Used planter 1",
stuffed animal.json:    "name": "Used planter 10",
```
This shows how you can call a tool manually. The formatting of the result when called manually may be different the the formatting of the result when called through the agent.

Using calculate in test_projects/markdown-compiler.

``` bash
$ cd test_projects/markdown-compiler
$ chat
chat> (40*2 + 77)
157
chat> Subtract 45 from the previous result
112
```
This example shows how you can use previous caculate results in new expressions.