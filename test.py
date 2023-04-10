import json


def handle(data, name):
    if len(data) > 1:
        return False
    else:
        return data[0]['name'] == name


def main():
    all = {}
    for i in range(0, 50):
        output = {'compreface_valid': 0, 'compreface_percent': 0, 'deepstack_valid': 0, 'deepstack_percent': 0,
                  'total': 0}
        f = open(f"result{i}.json")
        data = json.loads(f.read())
        f.close()
        for key in data.keys():
            for test in data[key]:
                output['total'] += 1
                if handle(test['compreface'], key.lower()):
                    output['compreface_valid'] += 1
                if handle(test['deepstack'], key.lower()):
                    output['deepstack_valid'] += 1

        output['compreface_percent'] = (output['compreface_valid'] / output['total']) * 100
        output['deepstack_percent'] = (output['deepstack_valid'] / output['total']) * 100
        all[i + 1] = output
    print(all)
    w = open("result.json", "w")
    w.write(json.dumps(all))
    w.close()


if __name__ == '__main__':
    main()
