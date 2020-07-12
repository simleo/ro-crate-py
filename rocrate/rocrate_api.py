#!/usr/bin/env python

## Copyright 2019-2020 The University of Manchester, UK
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import io
import json
import os
import tempfile
from contextlib import redirect_stdout

import rocrate.rocrate as roc
from galaxy2cwl import get_cwl_interface

def make_workflow_rocrate(workflow_path,wf_type,include_files=[],cwl=None,diagram=None):

    #returns a complete ROCrate object corresponding to a Workflow template file
    # wf_type: Galaxy, CWL , Nextflow..
    # cwl: CWL/CWL-Abstract representation of the workflow. If the
    # diagram: an image/graphical workflow representation.
    #         If a CWL/CWLAbstract file is provided then this is generated using cwltool
    #abs_path = os.path.abspath(workflow_path)
    wf_crate = roc.ROCrate()
    # add main workflow file
    file_name = os.path.basename(workflow_path)
    wf_file = wf_crate.add_file(workflow_path,file_name)  # should I add it in a special path within the crate?
    wf_crate.set_main_entity(wf_file)
    #print(wf_file.id)
    if wf_type != 'CWL':
        if cwl:
            #add cwl file to crate
            wf_crate.add_file(cwl)  # should add it in a special path within the crate?
        elif wf_type == 'Galaxy':
            #create cwl_abstract
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as cwl_abstract_out:
                with redirect_stdout(cwl_abstract_out):
                    get_cwl_interface.main(['1',workflow_path])
            wf_crate.add_file(cwl_abstract_out.name, 'abstract_wf.cwl')

    for file_entry in include_files:
        wf_crate.add_file(file_entry)
    return wf_crate


