#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

"""
Adapted from here:
https://gist.github.com/riga/157625f7323e529a60d83ef5bec68c1d
Based on this discussion:
https://cms-talk.web.cern.ch/t/nanoaod-merge-datasets-with-duplicate-event-removal/26376
"""

"""
Script that merges the Events tree of NanoAOD files,
removing duplicates identified by event number, run number and luminosity block.
"""

import os
import math
from functools import partial
from typing import Any
from typing import List
import numpy as np
import awkward as ak
import uproot

try:
    import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def haddnanodata(
    output_path: str,
    input_paths: List[str],
    force: bool = False,
    tree_name: str = "Events",
    keep_branches: List[str] | None = None,
    step_size: int = 100000,
    verbose: bool = False,
) -> tuple[int, int]:

    """
    Joins multiple NanoAOD files in the list *input_paths*,
    removes duplicates identified by the (event, run, luminosityBlock) triplet,
    and saves the joined file at *output_path*.
    The output file will only contain a tree named *tree_name*, i.e., any other
    objects contained in one of the input files are dropped.
    In case a file already exists at *output_path*, an Exception is thrown,
    unless *force* is set to True (in which case the existing file is overwritten).
    The output file is filled in chunks with a certain *step_size*,
    each one resulting in a new basket in the output file. 
    It is recommended to choose this value as large as possible 
    (depending on the available memory), to speed up the merging process
    but also to create files that are faster to read.
    *keep_branches* is forwarded as *filter_name* to :py:meth:`uproot.TTree.iterate`
    to select which branches to keep.
    If set, the three index branches (event, run, luminosityBlock) should be accepted.
    For more info, see https://uproot.readthedocs.io/en/latest/uproot.behaviors.TTree.TTree.html#arrays
    The number of written and overlapping events is returned in a 2-tuple.
    """
    
    # expand variables
    expand = lambda path: os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    input_paths = [expand(input_path) for input_path in input_paths]
    output_path = expand(output_path)

    # check if all input files exist
    for input_path in input_paths:
        if not os.path.isfile(input_path):
            msg = 'ERROR: input file {} does not seem to exist.'.format(input_path)
            raise Exception(msg)

    # define index columns and check if they are contained in branches to keep
    index_columns = ["event", "run", "luminosityBlock"]
    if keep_branches is not None:
        for index_column in index_columns:
            if index_column not in keep_branches:
                msg = 'ERROR: keep_branches does not contain required index branches {}.'.format(index_columns)
                raise Exception(msg)

    # prepare the output
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    elif os.path.exists(output_path):
        if not force:
            msg = 'ERROR: output file {} already exists.'.format(output_path)
            msg += ' Either remove it or run with force=True to overwrite it.'
            raise Exception(msg)
        else:
            msg = 'WARNING: overwriting existing file {}...'.format(output_path)
            print(msg)
            os.remove(output_path)
    output_file = uproot.create(output_path)

    # get input trees
    trees = [uproot.open(input_path)[tree_name] for input_path in input_paths]
    tree1 = trees[0]

    # read index columns over the full reference file
    index = tree1.arrays(index_columns)

    # prepare counts
    n_written = 0
    n_overlap = 0

    # iteration helper
    def iterate(tree, ntree, ntrees):
        if verbose:
            print(f"Iterating through tree {ntree}/{ntrees} with {tree.num_entries} events")
        progress = (
            partial(tqdm.tqdm, total=int(math.ceil(tree.num_entries / step_size)))
            if( verbose and HAS_TQDM ) else (lambda gen: gen) )
        return progress(tree.iterate(step_size=step_size, filter_name=keep_branches))

    # fill chunks of the first tree
    for chunk in iterate(tree1, 1, len(trees)):
        # update counts
        n_written += len(chunk)
        # extend the output tree
        chunk = dict(zip(chunk.fields, ak.unzip(chunk)))
        if tree_name in output_file: output_file[tree_name].extend(chunk)
        else: output_file[tree_name] = chunk

    # fill chunks of the other trees
    for idx, tree in enumerate(trees[1:]):
        for chunk in iterate(tree, idx+2, len(trees)):
            # determine a mask of events in tree that are also in tree1
            mask = np.isin(chunk[index_columns], index, assume_unique=True)
            chunk = chunk[~mask]
            # update counts
            n_written += len(chunk)
            n_overlap += ak.sum(mask)
            # skip the chunk if all events are overlapping
            if ak.all(mask): continue
            # extend the output tree
            chunk = dict(zip(chunk.fields, ak.unzip(chunk)))
            output_file[tree_name].extend(chunk)
            # update the index
            chunkindex = {key: chunk[key] for key in index_columns}
            chunkindex = ak.Array(chunkindex)
            index = ak.concatenate((index, chunkindex))

    if verbose:
        print(f"written {n_written} and found {n_overlap} overlapping event(s)")

    return n_written, n_overlap


if __name__ == "__main__":
   
    # read command line arguments 
    import argparse
    parser = argparse.ArgumentParser(
        description="joins NanoAOD files and removes duplicate events",
    )
    parser.add_argument(
        "-o", "--outputfile",
        help="Path to the output file to be created",
    )
    parser.add_argument(
        "-i", "--inputfiles", nargs='+',
        help="Path to input files to merge",
    )
    parser.add_argument(
        "-f", "--force", default=False, action='store_true',
        help="Whether to overwrite output file if it already exists",
    )
    parser.add_argument(
        "--tree",
        "-t",
        default="Events",
        help="name of the trees to merge and create; default: Events",
    )
    parser.add_argument(
        "--step-size",
        "-s",
        type=int,
        default=100000,
        help="step size for iterations; default: 100000",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=False, action="store_true",
        help="verbose output, potentially with tqdm if installed",
    )
    parser.add_argument(
        "--test",
        default=False, action="store_true",
        help="verbose output, potentially with tqdm if installed",
    )
    args = parser.parse_args()

    # define branches to keep in output file
    keep_branches = None
    if args.test:
        keep_branches = ["event", "run", "luminosityBlock", "nMuon", "nElectron"]

    # merge the files
    haddnanodata(
        output_path=args.outputfile,
        input_paths=args.inputfiles,
        force=args.force,
        tree_name=args.tree,
        keep_branches=keep_branches,
        step_size=args.step_size,
        verbose=args.verbose )
