# nyaa-bot
This is a line bot based on python, with some uselessful function :p

## Get start
There's some variables to set before first launch in `modules/base/datacenter.py` and `modules/base/module.py`:  
- __line_bot_api  
Enter your line bot's token
- __user_id_default  
Enter your user id shows in your bot's setting page, since line bot cannot get provider's id for some reason idk :(


## Instruction
There's some file in `base` folder:
- `datacenter.py`  
Receive and transfer data between modules
- `data.py`  
Describe type of data modules to deal with
- `module.py`  
(Almost) Every module's base, providing basic fuction for use

if you want to add functionality to your bot, just add new python file to `modules` folder and create new class based on `ModuleBase` like this:

``` python
from .base import DataType, ModuleBase, ModuleData
class NotATestModule(ModuleBase):
    keywords = ['OωO', ' {1}NotTest']
    def text_message_user(self, reply_token, text_message, profile):
        pass
```

~~To be continew~~