#!/usr/bin/env python3

"""
SPDX-License-Identifier: GPL-2.0-or-later

Copyright 2022 VMware Inc, Tzvetomir Stoyanov (VMware) <tz.stoyanov@gmail.com>
"""

import sys, os
import tracecruncher.ftracepy as ft
import tc_base as tc

script_description = "Trace system calls, used by given container"
args_description = """
-s, --syscall [SYSCALL ...] : list of System call names to be traced, optional argument.
                              If no system calls are specified, all available are traced."""

class syscall_tracer(tc.tracer):
    def __init__(self, description):
        self.syscalls=[]
        super().__init__(prog_desc=script_description, args_desc=args_description)
        self.parser.add_argument('-s', '--syscall', nargs='+', dest='syscall',
                                 help="list of System call names to be traced, optional")

    def parse(self):
        self.parse_arguments()
        events = ft.available_system_events(system='syscalls', sort=False)
        if self.args.syscall:
          for s in self.args.syscall:
            if s in events:
              self.syscalls.append(s)
            elif "sys_enter_"+s in events:
              self.syscalls.append("sys_enter_"+s)
            else:
              raise ValueError("Event", s, "is not available in the system")
        else:
          for s in events:
            if "sys_enter_" in s:
              self.syscalls.append(s)
    def filterParents(self):
        filter=""
        for p in self.args.parent:
            if filter == "":
                filter = 'common_pid != {0}'.format(p)
            else:
                filter += '&& common_pid != {0}'.format(p)
        if filter != "":
           ft.set_event_filter(instance=self.instance, system='syscalls', filter=filter)
    def trace(self):
        if self.syscalls:
          events = self.syscalls
        else:
          events = ['all']
        ft.enable_events(instance=self.instance, events={'syscalls': events})
        if self.args.parent:
            self.filterParents()
        self.run_trace()
        ft.disable_events(instance=self.instance, events={'syscalls': events})
        ft.clear_event_filter(instance=self.instance, system='syscalls')

if __name__ == "__main__":
    scall_tracer = syscall_tracer(description=script_description)
    scall_tracer.parse()
    scall_tracer.trace()

