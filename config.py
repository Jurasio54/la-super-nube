import os
import ProxyCloud

BOT_TOKEN =  os.environ.get('bot_token','5495079265:AAHjhcna03KLCpc2qnYON49x2RCzV4Kn_O0')
API_ID =  os.environ.get('api_id','15472343')
API_HASH = os.environ.get('api_hash','6817c82fe0b762ed91999f49cd17f7d7')
SPLIT_FILE = 1024 * 1024 * int(os.environ.get('split_file','99'))
ROOT_PATH = 'root/'
ACCES_USERS = os.environ.get('tl_admin_user','demian2008').split(';')
PROXY = ProxyCloud.parse(os.environ.get('proxy_enc','http://KFGKJDYGJKLHFIYEKGIGCGYJKDEFLJRGDKLJDJLI'))

if PROXY:
  print(f'Proxy {PROXY.as_dict_proxy()}')
