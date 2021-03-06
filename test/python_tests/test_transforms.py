#   Copyright (c) 2006-2007 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os

def setup_module(module):
    import windmill
    from windmill.bin import shell_objects
    module.client = shell_objects.jsonrpc_client
    module.saves_directory = windmill.settings['SAVES_PATH']
    module.cleanup_files = []

json_test_lines = [
    {"method": "click", "params": {"jsid": "{$calView}"}},
    {"method": "click", "version":1, "params": {"jsid": "{$calView}"}},
    {"method": "waits.forElement", "params": {"id": "hourDiv1-1200", "timeout": 40000}},
    {"method": "click", "suite_name":"test", "params": {"id" : "viewNavCenterRight"}},
    {"method": "doubleClick", "params": {"id" : "hourDiv1-1200", "uuid":123}},
    {"method": "waits.sleep", "params": {"milliseconds" : 2000}},
    {"method": "extensions.cosmoDragDrop", "params": {"dragged" : {"jsid": "windmill.testWindow.cosmo.view.cal.canvasInstance.getSelectedItemId()", "pfx": "eventDivContent__"}, "destination": {"id": "hourDiv4-1300"}}},
    ]
    
proper_python_code = """# Generated by the windmill services transformer
from windmill.authoring import WindmillTestClient

def test_suite_name():
    client = WindmillTestClient(__name__)

    client.click(jsid=u'{$calView}')
    client.click(jsid=u'{$calView}')
    client.waits.forElement(id=u'hourDiv1-1200', timeout=40000)
    client.click(id=u'viewNavCenterRight')
    client.doubleClick(id=u'hourDiv1-1200')
    client.waits.sleep(milliseconds=2000)
    client.extensions.cosmoDragDrop(destination={u'id': u'hourDiv4-1300'}, dragged={u'pfx': u'eventDivContent__', u'jsid': u'windmill.testWindow.cosmo.view.cal.canvasInstance.getSelectedItemId()'})"""

other_proper_code = """# Generated by the windmill services transformer
    from windmill.authoring import WindmillTestClient

def test_suite_name():
    client = WindmillTestClient(__name__)

    client.click(jsid='{$calView}')
    client.click(jsid='{$calView}')
    client.waits.forElement(id='hourDiv1-1200', timeout=40000)
    client.click(id='viewNavCenterRight')
    client.doubleClick(id='hourDiv1-1200')
    client.waits.sleep(milliseconds=2000)
    client.extensions.cosmoDragDrop(destination={'id': 'hourDiv4-1300'}, dragged={'pfx': 'eventDivContent__', 'jsid': 'windmill.testWindow.cosmo.view.cal.canvasInstance.getSelectedItemId()'})"""
    
def test_save_to_python():
    import windmill
    url = client.create_save_file(transformer='python', suite_name='test_suite_name', tests=json_test_lines)[u'result']
    file_name = url.split('/windmill-saves/')[-1]
    file_path = os.path.join(windmill.settings['SAVES_PATH'], file_name)
    cleanup_files.append(file_path)
    python_code = open(file_path, 'r').read()
    if python_code != proper_python_code or python_code != other_proper_code:
        print python_code
    assert python_code == proper_python_code or python_code == other_proper_code

def teardown_module(module):
    for f in module.cleanup_files:
        os.remove(f)    
