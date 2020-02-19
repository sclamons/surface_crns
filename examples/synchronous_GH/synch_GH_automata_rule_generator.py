# (self_state, neighbor_active?):new_state
rule_map = {('Q', 'y'):'A',
            ('Q', 'n'):'Q',
            ('A', 'y'):'R',
            ('A', 'n'):'R',
            ('R', 'y'):'Q',
            ('R', 'n'):'Q'}

direction_pairs = {'R':'L',
                   'U':'D',
                   'L':'R',
                   'D':'U'}
direction_transitions = {'U':'R',
                         'L':'U',
                         'D':'L',
                         'R':'D'}
colormap = {'Q':'(240, 240, 240)',
            'A':'(44,127,184)',
            'R':'(127,205,187)',
            'edge':'(160,160,160)'}
all_states = ['Q', 'A', 'R']

def main():
    '''
    node state definition:
                <self_state>_<direction>_<position>_<states_seen>
    edge state definition:
                Edge_<direction> (Edges are non-activating)
    '''
    transition_rule_file = \
            open("GH_spinning_arrow_rules.txt", 'w')
    colormap_file = open("GH_spinning_arrow_colormap.txt",'w')

    # Write colormap rule for edge nodes separately.
    colormap_file.write('{Edge} ')
    first_color = True
    for direction in direction_pairs.keys():
        if first_color:
            first_color = False
        else:
            colormap_file.write(', ')
        colormap_file.write('Edge_' + direction)
    colormap_file.write(": " + colormap['edge'] + "\n")

    # Transition rules and colormaps:
    for direction in direction_pairs.keys():
        for self_state in all_states:
            for location in [str(i) for i in range(1,10)]:
                neighbor_direction = direction_pairs(direction)
                neighbor_position = find_neighbor_position(direction, position)
                for neighbor_state in all_states:
                    states_seen = ""
                    if direction == "U":
                        transition_rule_file.write(f"(1) {")


    # Close out files.
    transition_rule_file.close()
    colormap_file.close()

if __name__ == "__main__":
    main()











    '''
    node state definition:
                <self_state>_<direction>_<position>_<I become active?>
    edge state definition:
                Edge_<direction> (Edges are non-activating)
    '''
    transition_rule_file = \
            open("GH_spinning_arrow_rules.txt", 'w')
    colormap_file = open("GH_spinning_arrow_colormap.txt",'w')

    # Write colormap rule for edge nodes separately
    colormap_file.write('{Edge} ')
    first_color = True
    for direction in direction_pairs.keys():
        if first_color:
            first_color = False
        else:
            colormap_file.write(', ')
        colormap_file.write('Edge_' + direction)
    colormap_file.write(": " + colormap['edge'] + "\n")

    # Write transition rules and colormap rules for non-edge nodes.
    for self_state in ['Q', 'A', 'R']:
        colormap_file.write('{State ' + self_state + '} ')
        first_color = True
        for position in ['1','2','3','4','5','6','7','8', '9']:
            for activate in ['y', 'n']:
                for direction in direction_pairs.keys():
                    # State change rule for updating state and reseting the
                    # spinner
                    # <self_state>_<direction>_<position>_<I become active?>
                    transition_rule_file.write('(1) ' +
                                    self_state + '_' +
                                    direction + '_' + 
                                    position + '_' +
                                    'None_' +
                                    neighbor_count +
                                    ' -> ' +
                                    rule_map[(self_state, neighbor_count)]+'_'+
                                    location + parity + '_' +
                                    start_direction + '_n\n')
                    if first_color:
                        first_color = False
                    else:
                        colormap_file.write(', ')
                    colormap_file.write(self_state + '_' + location + parity +
                                            '_None' + '_' + neighbor_count)
                    # Write colormap rule
                    if first_color:
                        first_color = False
                    else:
                        colormap_file.write(', ')
                    colormap_file.write(self_state + '_' + location +
                                        parity + '_' + direction + '_' +
                                        neighbor_count)

                    # Rules for nodes bordering on edge nodes.
                    edge_transition_string = edge_rule_string(self_state,
                                                        location,
                                                        parity,
                                                        direction,
                                                        neighbor_count)
                    transition_rule_file.write(edge_transition_string +
                                               '\n')

                    for neighbor_neighbor_count in ['y', 'n']:
                        for neighbor_state in ['Q', 'A', 'R']:
                            transition_string = transition_rule_string(
                                                    self_state,
                                                    location,
                                                    parity,
                                                    direction,
                                                    neighbor_count,
                                                    neighbor_state,
                                                    neighbor_neighbor_count)
                            #print(transition_string)
                            transition_rule_file.write(transition_string +
                                                           "\n")
        colormap_file.write(": " + colormap[self_state] + "\n")

    transition_rule_file.close()
    colormap_file.close()

def transition_rule_string(self_state, location, parity, direction,
                           neighbor_count, neighbor_state,
                           neighbor_neighbor_count):
    neighbor_location = -1
    if parity == 'a':
        neighbor_parity = 'b'
    else:
        neighbor_parity = 'a'
    next_direction = direction_transitions[direction]
    neighbor_next_direction = direction_transitions[direction_pairs[direction]]
    if direction == 'U':
        neighbor_location = str((int(location) - 3) % 9)
    elif direction == 'L':
        neighbor_location = str(((int(location)-1)%3 + ((int(location)//3)*3)))
        if parity == 'b':
            next_direction = 'None'
            neighbor_next_direction = 'None'
    elif direction == 'D':
        neighbor_location = str((int(location) + 3) % 9)
    elif direction == 'R':
        neighbor_location = str(((int(location)+1)%3) + ((int(location)//3)*3))
        if parity == 'a':
            next_direction = 'None'
            neighbor_next_direction = 'None'

    if neighbor_count == 'n' and (self_state != 'Q' or neighbor_state != 'A'):
        active = 'n'
    else:
        active = 'y'

    if neighbor_neighbor_count == 'n' and (neighbor_state != 'Q' or self_state != 'A'):
        neighbor_active = 'n'
    else:
        neighbor_active = 'y'

    return ('(1) ' +
            self_state + '_' +
            location + parity + '_' +
            direction + '_' +
            neighbor_count +
            ' + ' +
            neighbor_state + '_' +
            neighbor_location + neighbor_parity + '_' +
            direction_pairs[direction] + '_' +
            neighbor_neighbor_count +
            ' -> ' +
            self_state + '_' +
            location + parity + '_' +
            next_direction + '_' +
            active +
            ' + ' +
            neighbor_state + '_' +
            neighbor_location + neighbor_parity + '_' +
            neighbor_next_direction + '_' +
            neighbor_active
           )

def edge_rule_string(self_state, location, parity, direction, neighbor_count):
    next_direction = direction_transitions[direction]
    if direction == 'L' and parity == 'b':
        next_direction = 'None'
    elif direction == 'R' and parity == 'a':
        next_direction = 'None'

    return ('(1) ' +
            self_state + '_' +
            location + parity + '_' +
            direction + '_' +
            neighbor_count +
            ' + ' +
            'Edge_' + direction_pairs[direction] +
            ' -> ' +
            self_state + '_' +
            location + parity + '_' +
            next_direction + '_' +
            neighbor_count +
            ' + ' +
            'Edge_' + direction_pairs[direction]
           )

