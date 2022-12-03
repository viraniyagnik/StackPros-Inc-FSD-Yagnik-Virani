from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)

childs = None
root = {
    "type": "dir",
    "children": {
        "home": {
            "type": "dir",
            "children": {
                "myname": {
                    "type": "dir",
                    "children": {
                        "filea.txt": {
                            "type": "file"
                        },
                        "fileb.txt": {
                            "type": "file"
                        }
                    }
                },
                "home_2": {
                    "type": "dir",
                    "children": {
                        "filea.txt": {
                            "type": "file"
                        },
                        "fileb.txt": {
                            "type": "file"
                        }
                    }
                }
            }
        },
        "new_home": {
            "type": "dir",
            "children": {
                "filea.txt": {
                    "type": "file"
                },
                "fileb.txt": {
                    "type": "file"
                }
            }
        }
    }
}


# API to fetch whole directory structure
@ app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        return jsonify({'data': root})


def get_child_details(data):
    child_dirs = list(data.keys())
    global final_data
    final_data = []
    for dir in child_dirs:
        data_dict = dict()
        if data[dir]['type'] == 'dir':
            data_dict['name'] = dir
            data_dict['type'] = 'dir'
            print("==> data_dict: ", data_dict)
            final_data.append(data_dict)
        else:
            data_dict['name'] = dir
            data_dict['type'] = 'file'
            print("==> data_dict: ", data_dict)
            final_data.append(data_dict)
    return final_data


def get_child_dirs(data, of_dir):
    parent_dirs = list(data.keys())
    for dir in parent_dirs:
        if data[dir]['type'] == 'dir':
            print("===> Directory: ", dir)
            if dir == of_dir:
                childs = get_child_details(data[dir]['children'])
                print("===> childs: ", childs)
                # return childs
            else:
                get_child_dirs(data[dir]['children'], of_dir)
        else:
            print("===> File: ", dir)


# API to fetch children folders & files of given mypath
@ app.route('/path/<string:mypath>', methods=['GET'])
def disp(mypath):
    if mypath == "root":
        get_child_details(root["children"])
        return jsonify(final_data)
    else:
        get_child_dirs(root['children'], mypath)
        print("===> OUTSIDE: ", final_data)
        return jsonify(final_data)


# driver function
if __name__ == '__main__':

    app.run()
