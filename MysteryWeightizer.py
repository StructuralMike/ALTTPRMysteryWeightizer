import yaml
import random
import argparse

def roll_settings(weights,settings,points,sub = None):
    for setting,alternatives in weights.items():
        options = [x for x in list(alternatives.items()) if type(x[1]) == int]
        option = random.choice(options)
        if sub:
            settings[sub][setting] = {option[0]: 1}
        else:
            settings[setting] = {option[0]: 1}
        points += option[1]
    return settings,points

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-i', help='Path to the points weights file to use for rolling game settings')
    parser.add_argument('-o', help='Output path for the rolled mystery yaml')
    args = parser.parse_args()

    input_yaml = "weightizer_example.yml"
    output_file = "mystery_weighted.yaml"

    if args.i:
        input_yaml = args.i

    if args.o:
        output_file = args.o

    with open(input_yaml, "r", encoding='utf-8') as f:
        yaml_weights = yaml.load(f, Loader=yaml.SafeLoader)

    while True:
        settings = {'rom': {}, 'startinventory': {}}
        points = 0

        settings,points = roll_settings(yaml_weights['rom'], settings, points, sub='rom')
        settings,points = roll_settings(yaml_weights['world'], settings, points)

        if 'vanilla' not in settings['entrance_shuffle']:
            settings,points = roll_settings(yaml_weights['entrance'], settings, points)

        if 'vanilla' not in settings['door_shuffle']:
            settings,points = roll_settings(yaml_weights['doors'], settings, points)

        if 'vanilla' not in settings['overworld_shuffle'] or 'limited' in settings['overworld_crossed'] or 'chaos' in settings['overworld_crossed']:
            settings,points = roll_settings(yaml_weights['ow'], settings, points)

        if 'triforce-hunt' or 'ganonhunt' or 'trinity' in settings['goals']:
            settings,points = roll_settings(yaml_weights['tfh'], settings, points)

        if 'triforce-hunt' not in settings['goals'] and 'pedestal' not in settings['goals'] and 'dungeons' not in settings['goals']:
            settings,points = roll_settings(yaml_weights['ganon_goal'], settings, points)

        # Roll starting inventory
        min_points = yaml_weights['weight_options']['min_points']
        max_points = yaml_weights['weight_options']['max_points']
        max_items = yaml_weights['weight_options']['max_starting_items']
        if max_items > 0:
            available_items = [(item, weight) for item, weight in yaml_weights['startinventory'].items() if type(weight) == int]
            random.shuffle(available_items)
            for item, weight in available_items:
                if len(settings['startinventory']) >= max_items:
                    break
                if points+weight <= max_points and points+weight >= min_points:
                    settings['startinventory'][item] = {'on': 1}
                    points += weight
                    if random.random() < 0.5:
                        break
                    continue
                if points < min_points and weight > 0:
                    settings['startinventory'][item] = {'on': 1}
                    points += weight
                    continue
                if points > max_points and weight < 0:
                    settings['startinventory'][item] = {'on': 1}
                    points += weight
                    continue

        if points <= max_points and points >= min_points:
            break

    settings['description'] = 'Weightizer score: {} points'.format(points)

    print('Successfully generated mystery settings: {}'.format(output_file))

    with open(output_file, "w+", encoding='utf-8') as f:
        yaml.dump(settings,f, Dumper=yaml.SafeDumper, encoding='utf-8', allow_unicode=True, default_flow_style=False)

if __name__ == '__main__':
    main()