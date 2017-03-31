# About
Simple easy to use analyzer for the knesset protocol.
Required : python3+


# How to run?
  - Run `python unzip_protocols.py` to unzip the `committee-meetings-protocols.zip`
  - Run `analyze_protocols.py` - you should see two new files: `full_people_list.csv`,`person_to_positions.csv`
  - That's it!

# Workflow
  - Load all files in dir looking like `/committee_*.csv`
  - Try to extract all `מוזמנים`  from the protocols
  - for each person in each committee try to extract the following fields:
  - `"first_name", "last_name", "full_name", "position", "committee", "date", "work_place", "role", "raw_line"`
  - Create one file conatining all analyzed data: `full_people_list.csv`
  - Also try to find same person(full name) - with more then one position: `person_to_positions.csv`


### Development

Want to contribute? Great!
Feel free to open PR/Issue :)

License
----

MIT - **Free Software, Hell Yeah!**

[//]: #URLs

   [dill]: <https://github.com/joemccann/dillinger>
