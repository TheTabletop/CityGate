# CityGate
First off if you are using this on windows, stop it. Just stop it. This setup assumes a linux system (and preferably debian based). If don't have a linux system, and don't want to dual boot. Install [virtual box](https://www.virtualbox.org/wiki/Downloads), and then create a virtual machine with it with a [mint iso](https://www.linuxmint.com/download.php).

First off clone the repository and get the correct branch, you are going to want iteration2.
```bash
git clone https://github.com/TheTabletop/CityGate.git
cd CityGate
git checkout -b iteration2
git pull origin iteration2
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
pip install pymongo
pip install gunicorn
pip install requests
pip install falcon-jsonify
pip install falcon-cors
```
You also need to make sure you have a running instance of mongodb, to get this set up, please follow the directions [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

Now with all of this you will need two terminal windows open with the env activated (`source activate rfg-api`), one to start the app, `gunicorn app` and the other to run the tests `python -m unittest` or do manual curl/wget/httpie requests.
