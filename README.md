## Software Testing 2022
### Assignment: PROJ

Aim. In the context of software engineering, the roles of a developer and a tester are usually
separated; the developer is to write requirements and code and a tester is expected to
identify oversights in code and requirements. However, we believe that even if these two
roles are distinct, they are also complementary. Therefore, in this assignment, your group
will experience software testing from both perspectives. There will be some constraints, but
you will have enough freedom to craft your products and use the testing techniques and
approaches you learned about in this course.


Product idea #3. A Digital Dating Service (4 groups)
This project simulates a digital system that helps people to find a soulmate.
A person registers by specifying a name, age, gender, interests and preferred
gender to meet. Any registered member can query the system by specifying a
few match criteria. The system will provide the user with a list of potential
matches.

## Installation

```sh
$ git clone https://github.com/nikhilkc96/PROJ-SWT-2022/
$ cd PROJ-SWT-2022//
$ pip install -r requirements.txt
```
## Run 
```sh
$ python main.py
```

Build your app with the following command:
```sh
pyinstaller -F --add-data=database.json:. main.py
```


