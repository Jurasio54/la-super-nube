import os
import ProxyCloud

BOT_TOKEN =  os.environ.get('bot_token','5622213713:AAG8qjtClGTFXedeT5JJ88HWVL5u0SuHIUo')
API_ID =  os.environ.get('api_id','9951836')
API_HASH = os.environ.get('api_hash','472d5cbba1cedc12cd37e152ab8edbcc')
SPLIT_FILE = 1024 * 1024 * int(os.environ.get('split_file','99'))
ROOT_PATH = 'root/'
ACCES_USERS = os.environ.get('tl_admin_user','RichZC').split(';')
PROXY = ProxyCloud.parse(os.environ.get('proxy_enc','http://KADKFLCAJDJJKJJGDYFASDDJHNJGDADKDGLGDELI'))

if PROXY:
  print(f'Proxy {PROXY.as_dict_proxy()}')
