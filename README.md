Preliminary example of hopengine - a search engine for beer hops

---

Installation:

Make and activate a virtual environment. Clone this repository.

Run:
pip install -r requirements.txt
cd flaskapp1

Rename config.py.sample to config.py and make any needed changes.
The config file is setup to use sqlite.

Run:
python db_create.py
python test_data.py
python run.py

Visit localhost:5000

---

About:

db_create.py creates the tables.

test_data.py deletes any existing data in the tables and loads data from the sample data feed files.

run.py runs the flask debug server.

data_processing.py handles moving data from feed files into the models/db. It's called by test_data.py

app/ holds the flask files: views and models.