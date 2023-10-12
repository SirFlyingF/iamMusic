# iamMusic
## Intoduction
Music used to take up a lot of space. It occupied physical space in the form of vinyl disks, then CDs. Then came the internet when you could buy individual songs store thousands in a memory stick. When that wasn't enough, came the era of streaming along with a subscription model.

I am a bit old school and still get full albums to download. Albiet not too old to be mainintaing vinyls. As such I faced issues with storage. 

**IamMusic** was conceived out of the idea to stream my library from a Raspberry Pie attached permanently to my home router. While it only works within the wifi at home, it can easily be exposed to internet. It still has a long way to go in terms of features and obviously hosting. 

## How to use
iamMusic can be run in two ways:
1. Debug Mode : Run the main.py file do run the flask dev server. Can be used for debugging.
2. Production : Run the deploy.zsh in you zsh terminal. Command line arguements are of the form:
   deploy host:port db_un:db_pw:db_host:db_port:db_name loglevel logfilepath
   where:
   1. host:port is the ip address of the applicaion delimited by : character
   2. db_un:db_pw:db_host:db_port:db_name is the : delimited string for username, pasword, host, port and db_name respectively
   3. loglevel is a number from 1 to 4 both inclusive. Currently not implemented but need a value.
   4. logfilepath is where the logs will be written when implemented

Another thing to note is that, iamMusic is just the backend. I do plan to add static files at some point, however. For now you'll have to use your own front end to it.
