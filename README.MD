# haveibeenpwned_lastpass

Website https://haveibeenpwned.com provides a way for you to check whether some of your passwords/usernames were leaked during one of the many breaches of online services.
If you are like me, you have a LastPass account with way too many random passwords to check them manually. 
What this script does:

1. logs into LastPass and retrieves its vault
2. goes through your entries and checks passwords through the haveibeenpwned API ([actual plain passwords are not sent anywhere](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2#cloudflareprivacyandkanonymity))
3. compiles the results into a report for you to see if you actually were pwned

## Getting Started

1. install Python 3
2. install all the dependencies with `pip install -r requirements.txt`
3. run `python have_i_though.py` and go through the interactive prompt

## Acknowledgments

* [Have I Been Pwned](https://haveibeenpwned.com) service and its author Troy Hunt
* [lastpass-python](https://github.com/konomae/lastpass-python) with his unofficial API around LastPass
