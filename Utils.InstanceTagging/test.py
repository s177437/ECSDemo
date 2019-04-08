import os
import handler

os.environ['aws_tag_key'] = "Owner"
os.environ['aws_tag_value'] = "NameOfOwner"

print(os.environ.get('aws_tag_value'))
handler.handler(None, None)
