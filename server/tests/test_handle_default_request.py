import pytest
import json
import zlib
from datetime import datetime
from handlers import handle_default_request

data = {'action': 'dfgdf', 'time': 1564770979.592023, 'data': 'dfgfgdf'}

def test_handle_default_request(request):
    response = handle_default_request(zlib.compress(json.dumps(data).encode()))
    '''Test existing compressed object in result of function'''
    assert zlib.decompress(response) 
    


