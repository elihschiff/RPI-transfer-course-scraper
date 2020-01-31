# RPI-transfer-course-scraper

Due to how RPI keeps track of courses you can transfer in, you have to search by school and then see which classes they offer that RPI accepts for transfer credit.

This program allows you to search by specific course (EX: "WRIT 1110"), instead of by specific school, and see every school that offers a replacement transfer course that RPI accepts.

# Installing and running
Please note, I have only tested this on Arch Linux while it may work on other operating systems I do not have a way to test it. However, feel free to open an issue on the issue tracker for other operating systems and I will do my best to help.
### Installing

```bash
$ git clone https://github.com/elihschiff/RPI-transfer-course-scraper.git
$ cd RPI-transfer-course-scraper/
$ pip install bs4
$ pip install selenium
```

Make sure to also install the required webdriver. If you are on Arch linux you can run
```bash
$ sudo pacman -S geckodriver
```
for all other operating systems take a look at [this link](https://selenium-python.readthedocs.io/installation.html#drivers) and install the Firefox geckodriver

### Running

- To run the program simply run
```bash
$ python scrape.py
```
- Then enter a course code exactly as you wish to search (most likely all uppercase)

- When it asks for an output file name, provide a file unique file name (most likely .csv as that is what the program outputs)

    Here is an example:
  ```bash
  $ python scrape.py
  Enter the course id exactly as you see it on sis EX:'CSCI 1200' (capitalization is important): CSCI 2300
  CSCI 2300
  Enter the output file name: csci_2300.csv
  csci_2300.csv
  ```

- The program will then run through every state and then every country. Once it finishes you may open the csv file and view the results.

### Troubleshooting

- If the program crashes while running make sure you have enough ram by closing down other programs on your computer. I think there is a memory leak in my code or more likely the webdriver that has caused me issues in the past.

- Also note, if the program crashes you will need to delete the csv output file and restart the program from scratch, there is no way to start a scrape midway through.

- If this program was given to you by somebody at RPI along with my email, feel free to email me, I would be happy to help! I however do not want to make my email public here.
