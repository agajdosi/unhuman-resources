# Unhuman Resources

This is original code for the artistic intervention Unhuman Resources.
It mirrors news servers idnes.cz and lidovky.cz onto fake websites https://lidov.ky and https://l-dnes.cz which contains altered mentions of Andrej Babis, czech prime minister and the owner of idnes.cz and lidovky.cz.
To see some of the edited articles please visit randomly redirecting page: https://babis.media.

For english version please see one of five translated screenshots:
- https://babis.media/12
- https://babis.media/18
- https://babis.media/29
- https://babis.media/37
- https://babis.media/43

## Ugly code

This is not clean code, it's mean code.
Hard to read, hard to understand.
Not nice.
Chaotic.
It was a one man job.
And he was an artist.
Feared by dead line.
And so it is ugly.
There is visible time pressure in the architecture of whole application and style of the code.
And I am sorry for that.

It is just published "as it is":
- to archive the project,
- to share it with anybody interested about the artwork and its exact background,
- to prevent it from being bought and locked down in some stupid private collection,
- to support community not those who ruins it and wants to wash their dirty hands,
- to save myself from future temptations.

Share, reuse, modify, enjoy <3

## Cleaned fork

If you are interested in re-using this project for your purposes you should probably wait few weeks as I will publish cleaned up fork soon.


Link to cleaned fork will be published here soon.
I will do it.
I promise.
Bombard me with emails to accelarate the process.

## Run the project

### Prerequisites

1. Installed python3 and pip3
2. have port 8080 available (or use another available port)

Alternatively:

- use virtual environment `venv`, activate it with: `source ./venv/bin/activate` and then continue

### Local use

1. install needed packages with pip3:
   ```
    pip3 install tornado, requests, beautifulsoup4, tldextract, pysocks, lxml
   ```
2. run the application:
   1. to fake idnes.cz use: `python3 main.py -p 8080 -s localhost=idnes.cz -d True`
   2. to fake lidovky.cz use: `python3 main.py -p 8080 -s localhost=lidovky.cz -d True`
3. open browser and open address http://localhost:8080
   
### Problems
In case of any problem open an issue in this repository or throw me an email to andreas.gajdosik( a t )gmail.com.
