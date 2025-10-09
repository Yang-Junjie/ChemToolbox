import api.utils as utils

result = utils.find_element("Cu")
if result:
    print(result)
else:
    print("元素不存在")