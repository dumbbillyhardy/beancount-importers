# Overview
This is a set of custom-ish importers for the different bank and bank-like entities I have. They currently include: amex, chase, discover, and ynab.

## How I got Started
I previously kept track of all my finances through ynab, so I started with the importer I have here, renaming all of my accounts to match the beancount accounts
and renaming all my expense groups/categories to something that would be valid in beancount (emojis are currently invalid 😔). I then combed over this file
removing duplicates (mostly from account transfers) until everything matched up. I hope to eventually make a ynab exporter that will dedup the transfers so I
can just generate this file from scratch whenever I want. From there, the plan is to download csv's from my banks and figure out how to append to the main file,
taking backups along the way and making account balance assertions.

## How someone else should get started
Install all of the relevant (beancount)[https://beancount.github.io/docs/] stuff and then
clone this repo. Alter the `example_config.py` to something that makes sense to you.
You will also need to pip3 install dateutil and titlecase.

## Running
I keep all my files in `bank_downloads` (and don't commit it). The goal is to be able to point bean-extract at that and have it either regenerate everything (if
it is efficient enough) or smartly dedup and append to the main file. Until then, I download partial files from my bank and put the new transaction files in
the `working` folder. I then run `bean-extract config.py working/ >> finances.beancount` to get the new transactions.
