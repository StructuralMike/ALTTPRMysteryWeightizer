import yaml
import random
import argparse

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--i', help='Path to the points weights file to use for rolling game settings')
    parser.add_argument('--o', help='Output path for the rolled mystery yaml')
    args = parser.parse_args()

    if args.i:
        input_yaml = args.i
    else:
        input_yaml = "weightizer_example.yml"

    if args.o:
        output_file = args.o
    else:
        output_file = "mystery_weighted.yaml"

    with open(input_yaml, "r", encoding='utf-8') as f:
        yaml_weights = yaml.load(f, Loader=yaml.SafeLoader)

    while True:
        settings = {}
        points = 0

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
        try:
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
        except:
            pass # No (more) starting items available

        settings['rom'] = {}
        for setting,alternatives in yaml_weights['rom'].items():
            options = [x for x in list(alternatives.items()) if type(x[1]) == int]
            option = random.choice(options)
            settings['rom'][setting] = {option[0]: 1}
            points += option[1]
        
        if points <= yaml_weights['weight_options']['max_points'] and points >= yaml_weights['weight_options']['min_points']:
            break

    settings['description'] = 'Weightizer score: {} points'.format(points)

    print('Successfully generated mystery settings: {}'.format(output_file))

    with open(output_file, "w+", encoding='utf-8') as f:
        yaml.dump(settings,f, Dumper=yaml.SafeDumper, encoding='utf-8', allow_unicode=True, default_flow_style=False)

if __name__ == '__main__':
    main()