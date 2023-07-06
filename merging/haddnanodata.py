#!/usr/bin/env python3
# coding: utf-8

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

import sys
import os
import math
from functools import partial

import numpy as np
import awkward as ak
import uproot


def haddnanodata(
    output_path,
    input_paths,
    force = False,
    tree_name = "Events",
    keep_branches = None,
    step_size = 100000,
    verbose = False):
    """
    Joins multiple NanoAOD files in the list *input_paths*, removes duplicates
    identified by the (event, run, luminosityBlock) triplet, and saves the joined file at
    *output_path*.
    The output file will only contain a tree named *tree_name*, i.e., any other
    objects contained in one of the input files are dropped.
    In case a file already exists at *output_path*, an Exception is thrown,
    unless *force* is set to True (in which case the existing file is overwritten).
    The output file is filled in chunks with a certain *step_size*, each one resulting in a new
    basket in the output file. It is recommended to choose this value as large as possible (
    depending on the available memory), to speed up the merging process but also to create files
    that are faster to read.
    *keep_branches* is forwarded as *filter_name* to :py:meth:`uproot.TTree.iterate`
    to select which branches to keep. If set, the three index
    branches (event, run, luminosityBlock) should be accepted.
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
    firsttree = trees[0]

    # read index columns over the full reference file
    index_columns = ["event", "run", "luminosityBlock"]
    index = firsttree.arrays(index_columns)

    # prepare counts
    n_written = 0
    n_overlap = 0

    # fill chunks of the first tree
    print('Reading tree 1/{} (with {} events)...'.format(len(trees),firsttree.num_entries))
    for chunk in firsttree.iterate(step_size=step_size, filter_name=keep_branches):
        # update counts
        n_written += len(chunk)
        # extend the output tree
        chunk = dict(zip(chunk.fields, ak.unzip(chunk)))
        if tree_name in output_file: output_file[tree_name].extend(chunk)
        else: output_file[tree_name] = chunk

    # fill chunks of the other trees
    for idx, tree in enumerate(trees[1:]):
        print('Reading tree {}/{} (with {} events)...'.format(idx+2, len(trees), tree.num_entries))
        for chunk in tree.iterate(step_size=step_size, filter_name=keep_branches):
            # determine a mask of events in this tree that are duplicate
            mask = np.isin(chunk[index_columns], index, assume_unique=True)
            # find unique events
            chunk = chunk[~mask]
            # update counts
            n_written += len(chunk)
            n_overlap += ak.sum(mask)
            # skip the chunk if all events are overlapping
            if ak.all(mask): continue
            # extend the tree
            chunk = dict(zip(chunk.fields, ak.unzip(chunk)))
            output_file[tree_name].extend(chunk)
            # update the index
            chunkarray = ak.Array(chunk)
            index = ak.concatenate((index, chunkarray))

    # print number of written and overlapping events
    if verbose:
        print("Written {} and found {} overlapping event(s)".format(n_written, n_overlap))

    return (n_written, n_overlap)


if __name__ == "__main__":
    
    output_path = sys.argv[1]
    input_paths = sys.argv[2:]

    haddnanodata(
        output_path,
        input_paths,
        verbose=True)
