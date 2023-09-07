# iamMusic
## Intoduction
Music used to take up a lot of space. It occupied physical space in the form of vinyl disks, then CDs. Then came the internet when you could buy individual songs store thousands in a memory stick. When that wasn't enough, came the era of streaming along with a subscription model.

I am a bit old school and still get full albums to download. Albiet not too old to be mainintaing vinyls. As such I faced issues with storage. 

**IamMusic** was conceived out of the idea to stream my library from a Raspberry Pie attached permanently to my home router. While it only works within the wifi at home, it can easily be exposed to internet. It still has a long way to go in terms of features and obviously hosting. 

## How to use
iamMusic repo on GitHub is a basic flask app. It can be run on any WSGI server wherever you want. That part is intentionally left out. To get going however, you can simply run run-srvCore.py in python and it should launch flask's dev server. 

Another thing to note is that, iamMusic is just the backend. I do plan to add static files at some point, however. For now you'll have to use your own front end to it.