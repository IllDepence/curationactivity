""" Script to demo the generation of an AS2 Collection for Curations.
"""

import configparser
import hashlib
import json
import os
import sys
import uuid

from util import Curation
from util import ASCollection
from util import ASCollectionPage
from util import ActivityBuilder

def main():
    # parse config
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'environment' not in config.sections():
        print('Config file needs a [environment] section.')
        sys.exit(1)
    elif 'curation_folder' not in config['environment'] or \
         'as_folder' not in config['environment'] or \
         'collection_name' not in config['environment'] or \
         'base_uri' not in config['environment'] or \
         'actor' not in config['environment']:
        print(('Config section [environment] needs entries "curation_folder", '
               '"as_folder", "collection_name", "base_uri" and "actor".'))
        sys.exit(1)

    # set variables
    as_folder = config['environment']['as_folder']
    col_name = '{}.json'.format(config['environment']['collection_name'])
    col_path = '{}/{}'.format(as_folder, col_name)
    base_uri = config['environment']['base_uri']
    actor = interpret_actor(config['environment']['actor'])
    cur_files_pre = [f.path for f
                     in os.scandir(config['environment']['curation_folder'])
                     if f.is_file()]
    # skip unchanged files
    curation_files = []
    done_log = get_done_log()
    for cf in cur_files_pre:
        if cf in done_log.keys():
            with open(cf) as f:
                hesh = hashlib.sha256(bytes(f.read(), 'utf-8')).hexdigest()
                if done_log[cf] != hesh:
                    # old file but changed
                    curation_files.append(cf)
        else:
            # new file
            curation_files.append(cf)

    # setup collection
    if not os.path.exists(as_folder):
        os.makedirs(as_folder)
    if not os.path.exists(col_path):
        col_id = '{}/{}'.format(base_uri, col_name)
        col = ASCollection(col_id, col_path)
    else:
        # doesn't check if config has changed since files were saved
        with open(col_path) as f:
            col = ASCollection(None, col_path)
            col.restore_from_fs(as_folder)

    # parse Curations
    for path in curation_files:
        with open(path) as f:
            cur = Curation(None)
            cur.from_json(f.read())

        page_fn = 'page-{}.json'.format(uuid.uuid4())
        page_id = '{}/{}'.format(base_uri, page_fn)
        page = ASCollectionPage(page_id, '{}/{}'.format(as_folder, page_fn))

        # Create
        create = ActivityBuilder.build_create(cur.get_id(), actor=actor)
        page.add(create)
        # Reference
        for cid in cur.get_all_canvas_ids():
            ref = ActivityBuilder.build_reference(cur.get_id(), cid, actor=actor)
            page.add(ref)
        # Offerings
        for dic in cur.get_range_summary():
            range_id = dic.get('ran')
            manifest_id = dic.get('man')
            off = ActivityBuilder.build_offer(cur.get_id(), range_id,
                                              manifest_id, actor=actor)
            page.add(off)

        col.add(page)
        mark_done(path)

def interpret_actor(some_str):
    """ Try to interpret the actor set in config.ini.

        plain string in config ✔
        JSON object in config ✔
        JSON object linked in config (TODO)
    """

    valid_types = ['Application', 'Group', 'Organization', 'Person', 'Service']

    try:
        sth = json.loads(some_str)
        if sth.get('type') and sth.get('name') and \
                sth.get('type') in valid_types:
            return sth
        else:
            return some_str
    except:
        return some_str

def get_done_log():
    """ Load log of previously processed files into a dict.
    """

    if not os.path.exists('done_log'):
        return {}
    dic = {}
    with open('done_log') as f:
        for line in f:
            parts = line.split('\t')
            fn = parts[0].strip()
            hesh = parts[1].strip()
            dic[fn] = hesh
    return dic

def mark_done(cf):
    """ Mark a Curation file as processed.
    """

    with open(cf) as f:
        hesh = hashlib.sha256(bytes(f.read(), 'utf-8')).hexdigest()
    with open('done_log', 'a') as f:
        f.write('{}\t{}\n'.format(cf, hesh))

if __name__ == '__main__':
    main()
