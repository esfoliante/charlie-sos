# Charlie SOS

## Index

* <a href="#the-project">The project</a>
* <a href="#backstory">Backstory</a>
* <a href="#technologies">Technologies</a>
* <a href="#setup">Setup</a>
* <a href="#contribute">Contribute</a>

## The project

**Charlie SOS** is a simple python script made to be used, primarily, on a raspberry pi equipped with a microphone, with the purpose of detecting screams and loud noises (like doors being broken).

After detecting a loud noise, measured in decibels (dB), and adaptable to the needs of the user, an emergency protocol is fired where an SMS message is sent to trusted phone numbers, as well an e-mail (optional) with the same message.

Please take in consideration that this is not a commercial product and, therefore, the level of engineering is not the most advanced and the code is not 100% tested. Bugs may appear.

## Backstory

On one cold night my parents were in the bedroom, as usual, watching a show laying in bed while I was in the living room, a few meters away.

All of a sudden, my father felt a huge pain on his legs, and ended up passing out, leaving my mom desperate and helpless. She tried to scream my name, but during all the confusion she couldn't mutter the strength to scream loud enough.

Therefore I decided to create this project with this case, and many others in mind. This happened to my father, that had my mother, and I, to help him, but we can see this happening to older people, people with disabilities, or simply people that have a temporary sickness but don't have anyone nearby.

This is for those who can't have constant company but need to be taken care as much as we all do. I hope I can save someone's life.

> On a side note, my father is doing just fine. It was just a loose incident.

## Technologies

To develop this project, two main technologies were used:
* Python 3
* Docker

Docker exists here in this project, not as an overkill technology, but because I wanted this project to be easy to port to any device. Whether you're on a raspberry pi or on an old windows desktop that you have laying around, this project and be easily setup with one simple script execution.

## Setup

It's easy. Just easy.

### Installing dependencies

First off, make sure you have the dependencies installed in your system.
* Every Unix based operating system should have python installed, but, if not, you can install it by clicking [this link](https://www.python.org/downloads/).
* After installing Python, you should also install Docker, by clicking [this link](https://www.docker.com/)

### Changing your environment

The project demands that you update some environment variables for it to work.

To do this you simply start off by duplicating the ```.env.example``` file and renaming the duplicate to ```.env```.

After that, you should change all your environment variables to your own credentials.

If you don't know how to setup Twilio, you can find a guide on [this link](https://www.twilio.com/docs/libraries/reference/twilio-python/).

### Running the code

Finally, if it's your first time, you first need to run the command:

```bash
./setup.sh
```

The setup script will build your docker image based on the latest code, and proceed to run it for you automatically.

And you simply want to run the program again, after closing it, you simply run the command:

```bash
./start.sh
```

> On some Linux machines, you might have to execute the code as root, using the "sudo" keyword before executing the command


## Contribute

If you feel like you could benefit from X feature, start off by forking the repository and creating a pull request with your feature.

Make sure your branch follows the naming conventions, such as ```feat```, ```chore```, ```update```, and more (i.e: ```feat/image-detection```).

If you don't know how to write the code yourself, however, feel free to open an issue and we can discuss possible solutions for your problem!
