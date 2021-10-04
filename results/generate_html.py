#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021  The SymbiFlow Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC

import jinja2
from argparse import ArgumentParser
import os
import shutil

from generate_index_page import generate_index_html
from project_results import ProjectResults


def main():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('html'))

    parser = ArgumentParser()

    parser.add_argument(
        '-i',
        '--in-dir',
        type=str,
        help='Directory containing json data files'
    )
    parser.add_argument(
        '-o', '--out-dir', type=str, help='Save outputs in a given directory'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.in_dir):
        os.makedirs(args.in_dir)

    index_template = env.get_template('index.html')
    data_template = env.get_template('data.js')

    results = list()
    graph_pages = dict()

    for project_name in os.listdir(args.in_dir):
        project_dir = os.path.join(args.in_dir, project_name)
        if not os.path.isdir(project_dir):
            print(f'Skipping `{project_dir}` because it' 's not a directory.')
            continue

        # Do not filter failed tests
        project_results = ProjectResults(project_name, project_dir)
        results.append(project_results)

    index_page, data_page = generate_index_html(
        index_template, data_template, results
    )

    if args.out_dir:
        index_path = os.path.join(args.out_dir, 'index.html')
        with open(index_path, 'w') as out_file:
            out_file.write(index_page)

        data_dir = os.path.join(args.out_dir, 'data')

        os.makedirs(data_dir, exist_ok=True)
        with open(os.path.join(data_dir, 'data.js'), 'w') as out_file:
            out_file.write(data_page)


if __name__ == "__main__":
    main()
