#!/usr/bin/env python

"""
MyCopyTree.py

A clone of the distutils copytrtee, but adding an option to exclude certain patterns

"""
import fnmatch
from distutils.dir_util import *

def copy_tree (src, dst,
               preserve_mode=1,
               preserve_times=1,
               preserve_symlinks=0,
               update=False,
               verbose=False,
               dry_run=False,
               exclude_patterns=(),
               ):

    """Copy an entire directory tree 'src' to a new location 'dst'.  Both
       'src' and 'dst' must be directory names.  If 'src' is not a
       directory, raise DistutilsFileError.  If 'dst' does not exist, it is
       created with 'mkpath()'.  The end result of the copy is that every
       file in 'src' is copied to 'dst', and directories under 'src' are
       recursively copied to 'dst'.  Return the list of files that were
       copied or might have been copied, using their output name.  The
       return value is unaffected by 'update' or 'dry_run': it is simply
       the list of all files under 'src', with the names changed to be
       under 'dst'.

       'preserve_mode' and 'preserve_times' are the same as for
       'copy_file'; note that they only apply to regular files, not to
       directories.  If 'preserve_symlinks' is true, symlinks will be
       copied as symlinks (on platforms that support them!); otherwise
       (the default), the destination of the symlink will be copied.
       'update' and 'verbose' are the same as for 'copy_file'.
       
       exclude_patterns is a sequence of patterns to exclude. It will
       exclude an file or dir that has the pattern in it. this is not
       the least bit fancy, it uses the fnmatch module, so you can use
       unix-style shell matching ( *, ?, [seq], [!seq] )

       """
    
    if type(exclude_patterns) == str:
        exclude_patterns = [exclude_patterns,]

    from distutils.file_util import copy_file

    if not dry_run and not os.path.isdir(src):
        raise DistutilsFileError, \
              "cannot copy tree '%s': not a directory" % src
    try:
        names = os.listdir(src)
    except os.error, (errno, errstr):
        if dry_run:
            names = []
        else:
            raise DistutilsFileError, \
                  "error listing files in '%s': %s" % (src, errstr)

    if not dry_run:
        mkpath(dst)

    outputs = []

    for n in names:
        breaking = False
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(n, pattern):
                if verbose: print 'excluding:', n, "in:", src
                breaking = True
                break
        if breaking:
            continue
        src_name = os.path.join(src, n)
        dst_name = os.path.join(dst, n)

        if preserve_symlinks and os.path.islink(src_name):
            link_dest = os.readlink(src_name)
            log.info("linking %s -> %s", dst_name, link_dest)
            if not dry_run:
                os.symlink(link_dest, dst_name)
            outputs.append(dst_name)

        elif os.path.isdir(src_name):
            outputs.extend(
                copy_tree(src_name, dst_name, preserve_mode,
                          preserve_times, preserve_symlinks, update,
                          dry_run=dry_run,
                          exclude_patterns=exclude_patterns))
        else:
            copy_file(src_name, dst_name, preserve_mode,
                      preserve_times, update, dry_run=dry_run)
            outputs.append(dst_name)

    return outputs