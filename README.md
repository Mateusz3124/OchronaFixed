## Basic bank website

### How to start

you need to write following commands to start website:
```
git clone https://github.com/MatSobol/Bank.git
cd Bank
sudo docker-compose build
sudo docker-compose up
```
tutorial on how to install docker-compose:

https://docs.docker.com/compose/install/

### accounts for login:

first:

- authentication id: 12345678

- password: aA1!b4B1FG

second:

- authentication id: 87654321

- password: aA1!b4B1FG

### How it looks

Firstly you write your authentication id

![image](https://github.com/Mateusz3124/OchronaFixed/assets/95550799/c8c7c100-e28c-4be0-b030-afb807f7e677)

The minimum size of password is 10 so it only displays 11 blocks where black blocks are empty letters of password

![image](https://github.com/Mateusz3124/OchronaFixed/assets/95550799/7b565b61-cb4e-41f9-8eb3-dd65ff556dbd)

If the password is longer it will dynamically add blocks

![image](https://github.com/Mateusz3124/OchronaFixed/assets/95550799/4899fb91-b3af-47b4-8a9a-4d457a788105)

After login you can see main page of bank. For example:

![image](https://github.com/Mateusz3124/OchronaFixed/assets/95550799/c4beb18f-5974-4456-b0d5-a16aa22e2c56)

To encrypt data i use: sha

