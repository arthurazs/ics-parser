# ICS Parser in Python

Download ics (Internet Calendaring and Scheduling Core Object Specification) files into this project folders
and run `make r`. Example output:

```bash
$ tree
 .
├──  first.ics
├──  second.ics
├──  third.ics
├──  ics.py
├──  Makefile
├──  README.md
├──  ruff.toml

$ make r
python3 ics.py
2025/02/26 14:45~15:25 > first.ics
           https://teams.live.com/meet/123?p=abc > Title One...
2025/02/26 15:30~16:10 > second.ics
           https://teams.live.com/meet/456?p=qwe > Title Two...
2025/02/27 15:00~15:40 > third.ics
           https://teams.live.com/meet/789?p=zxc > Third title...
```

You may run `make c` to delete all ics files.


## Warning

This project was made for my personal use case.
Right now it only parses en-US summaries, and two time zones:

- E. South America Standard Time
- America/Sao_Paulo

But it should be very easy to change to your use case.
