# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/eeprom.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: eeprom.py '
from cxmanage_api.cli import get_nodes, get_tftp, run_command, prompt_yes

def eepromupdate_command(args):
    """Updates the EEPROM's on a cluster or host"""

    def validate_config():
        """Makes sure the system type is applicable to EEPROM updates"""
        for node in nodes:
            if 'Dual Node' not in node.get_versions().hardware_version:
                print 'ERROR: eepromupdate is only valid on TerraNova systems'
                return True

        return False

    def validate_images():
        """Makes sure all the necessary images have been provided"""
        if args.eeprom_location == 'node':
            for node in nodes:
                node_hw_ver = node.get_versions().hardware_version
                if 'Uplink' in node_hw_ver:
                    image = 'dual_uplink_node_%s' % (node.node_id % 4)
                else:
                    image = 'dual_node_%s' % (node.node_id % 4)
                if not [ img for img in args.images if image in img ]:
                    print 'ERROR: no valid image for node %s' % node.node_id
                    return True

        else:
            image = args.images[0]
            if 'tn_storage.single_slot' not in image:
                print 'ERROR: %s is an invalid image for slot EEPROM' % image
                return True
        return False

    def do_update():
        """Updates the EEPROM images"""
        if args.eeprom_location == 'node':
            for node in nodes:
                node_hw_ver = node.get_versions().hardware_version
                if 'Uplink' in node_hw_ver:
                    needed_image = 'dual_uplink_node_%s' % (node.node_id % 4)
                else:
                    needed_image = 'dual_node_%s' % (node.node_id % 4)
                image = [ img for img in args.images if needed_image in img ][0]
                print 'Updating node EEPROM on node %s' % node.node_id
                if args.verbose:
                    print '    %s' % image
                try:
                    node.update_node_eeprom(image)
                except Exception as err:
                    print 'ERROR: %s' % str(err)
                    return True

            print ''
        else:
            image = args.images[0]
            slot_nodes = [ node for node in nodes if node.node_id % 4 == 0 ]
            _, errors = run_command(args, slot_nodes, 'update_slot_eeprom', image)
            if errors:
                print 'ERROR: EEPROM update failed'
                return True
        return False

    if not args.all_nodes:
        if args.force:
            print 'WARNING: Updating EEPROM without --all-nodes' + ' is dangerous.'
        elif not prompt_yes('WARNING: Updating EEPROM without ' + '--all-nodes is dangerous. Continue?'):
            return 1
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp, verify_prompt=True)
    errors = validate_config()
    if not errors:
        errors = validate_images()
    if not errors:
        errors = do_update()
    if not args.quiet and not errors:
        print 'Command completed successfully.'
        print 'A power cycle is required for the update to take effect.\n'
    return errors