import yaml
import random
import argparse

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--i', help='Path to the points weights file to use for rolling game settings')
    args = parser.parse_args()

    if args.i:
        input_yaml = args.i
    else:
        input_yaml = "mystery_example.yml"
    with open(input_yaml, "r", encoding='utf-8') as f:
        yaml_weights = yaml.load(f, Loader=yaml.SafeLoader)

    while True:
        settings = {}
        points = 0

        settings['description'] = yaml_weights['description']

        for setting,alternatives in yaml_weights['world'].items():
            options = [x for x in list(alternatives.items()) if type(x[1]) == int]
            option = random.choice(options)
            settings[setting] = {option[0]: 1}
            points += option[1]

        if 'none' not in settings['entrance_shuffle']:
            for setting,alternatives in yaml_weights['entrance'].items():
                options = [x for x in list(alternatives.items()) if type(x[1]) == int]
                option = random.choice(options)
                settings[setting] = {option[0]: 1}
                points += option[1]

        if 'vanilla' not in settings['door_shuffle']:
            for setting,alternatives in yaml_weights['entrance'].items():
                options = [x for x in list(alternatives.items()) if type(x[1]) == int]
                option = random.choice(options)
                settings[setting] = {option[0]: 1}
                points += option[1]

        for setting,alternatives in yaml_weights['logic'].items():
            options = [x for x in list(alternatives.items()) if type(x[1]) == int]
            option = random.choice(options)
            settings[setting] = {option[0]: 1}
            points += option[1]

        if 'triforce-hunt' in settings['goals']:
            for setting,alternatives in yaml_weights['tfh'].items():
                options = [x for x in list(alternatives.items()) if type(x[1]) == int]
                option = random.choice(options)
                settings[setting] = {option[0]: 1}
                points += option[1]

        settings['startinventory'] = {}
        start_items = random.randint(yaml_weights['weight_options']['min_starting_items'],yaml_weights['weight_options']['max_starting_items'])
        item_choices = []
        for setting,alternatives in yaml_weights['startinventory'].items():
            if 'on' in alternatives and type(alternatives['on']) == int:
                item_choices.append(setting)
        random.shuffle(item_choices)
        while start_items > len(settings['startinventory']):
            item = item_choices.pop()
            options = [x for x in list(yaml_weights['startinventory'][item].items()) if type(x[1]) == int]
            option = random.choice(options)
            settings['startinventory'][item] = {option[0]: 1}
            points += option[1]

        settings['rom'] = {}
        for setting,alternatives in yaml_weights['rom'].items():
            options = [x for x in list(alternatives.items()) if type(x[1]) == int]
            option = random.choice(options)
            settings['rom'][setting] = {option[0]: 1}
            points += option[1]
        
        if points <= yaml_weights['weight_options']['max_points'] and points >= yaml_weights['weight_options']['min_points']:
            break

    print('Generated settings scoring {} points'.format(points))

    output_file = "mystery_weighted.yaml"
    with open(output_file, "w+", encoding='utf-8') as f:
        yaml.dump(settings,f, Dumper=yaml.SafeDumper, encoding='utf-8', allow_unicode=True, default_flow_style=False)

if __name__ == '__main__':
    main()