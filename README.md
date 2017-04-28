# CityGate
First off if you are using this on windows, stop it. Just stop it. This setup assumes a linux system (and preferably debian based). If don't have a linux system, and don't want to dual boot. Install [virtual box](https://www.virtualbox.org/wiki/Downloads), and then create a virtual machine with it with a [mint iso](https://www.linuxmint.com/download.php).

First off clone the repository and get the correct branch, you are going to want iteration2.
```bash
git clone https://github.com/TheTabletop/CityGate.git
cd CityGate
git checkout -b PokerProTestingBranch
git pull origin PokerProTestingBranch
```

If you don't have conda, do the following to download and build miniconda.
```bash
wget http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
```

Note, it is advisable that you also add the `export PATH=...` line above to your .bash_profile.

Now we need to create a new conda environment.
`conda create -n rfg-api python=3.4`

now let's activate the environment and install a few other dependencies.
```bash
source activate rfg-api
conda install pip
pip install falcon
pip install bson
pip install ipython
pip install pymongo
pip install gunicorn
pip install httpie
pip install msgpack-python
pip install falcon-jsonify
pip install falcon-cors
pip install requests
```
You also need to make sure you have a running instance of mongodb, to get this set up, please follow the directions [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

Now with all of this you will need two terminal windows open with the env activated (`source activate rfg-api`), one to start the app, `gunicorn app` and the other to run the tests `python -m unittest` or do manual testing by doing http requests with the python `requests` lib.

## Using python 'requests' lib

After you have the api running by following the above steps open a second terminal and activate the virtual env with `source activate rfg-api`. After that is done, start up python by typing `python` and pressing enter. Then from your terminal you can do the following.

```python
import requests
import json

params = {'email':'example@gmail.com', 'playername': 'FooBar', 'heroname': 'Foo the Bar(d)','games': ['D&D 5e', '7th Sea', 'GURPS', 'Iron Kingdoms', 'Blood Bowl'], 'key':'FooBardIsBestBard', 'backstory': 'Foo was the son of a baker with a temper and a whore'}
r = requests.post('http://127.0.0.1:8000/hero/create', data=json.dumps(params))

print(r)
# status[202]
print(r.json())
# {'success': 'Created a hero.', 'uhid': '<this is a uhid, just pretend>'}
print(r.text)
# {"success": "Created a hero.", "uhid": "<this is a uhid, just pretend>"}
```

If something goes wrong using `print(r.json())` should help. You can also checkout the gunicorn terminal window as if there was a server error, it should print out the logs there. For more on `requests` check out the lib's documentation [here](http://docs.python-requests.org/en/master/).
