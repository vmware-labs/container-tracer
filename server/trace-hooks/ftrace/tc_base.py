#!/usr/bin/env python3

"""
SPDX-License-Identifier: CC-BY-4.0

Copyright 2022 VMware Inc, Tzvetomir Stoyanov (VMware) <tz.stoyanov@gmail.com>
"""

import argparse
import tracecruncher.ftracepy as ft

class tracer:
    def __init__(self, prog_desc, args_desc):
        self.proc_description = prog_desc
        self.args_description = args_desc
        self.duration = 0
        self.instance = None
        self.parser = argparse.ArgumentParser(description=prog_desc)
        self.parser.add_argument('-p', '--pid', nargs='*', dest='pids', type=int,
                                 help="list of Process IDs to be traced, mandatory argument")
        self.parser.add_argument('-i', '--instance', nargs=1, dest='instance',
                                 help="Name of the trace instance used for tracing, optional argument")
        self.parser.add_argument('-t', '--time', nargs=1, dest='time', type=int,
                                 help="Duration of the trace in milliseconds, optional argument")
        self.parser.add_argument('--describe', action='store_true', dest='describe',
                                 help="Description of the script, displayed to the user")

    def parse_arguments(self):
        self.args = self.parser.parse_args()
        if self.args.describe:
            print(self.proc_description)
            print(self.args_description)
            print("-t, --time TIME : Duration of the trace in milliseconds, optional argument")
            exit(0)
        if self.args.time:
            self.duration = self.args.time[0]
        if self.args.instance:
          try:
            self.instance = ft.find_instance(self.args.instance[0])
          except:
            self.instance = ft.create_instance(tracing_on=False, name=self.args.instance[0])
        else:
          self.instance = ft.create_instance(tracing_on=False)
        if not self.args.pids:
          raise ValueError("No PIDs are provided.")
    def run_trace(self):
        ft.enable_option(option="event-fork", instance=self.instance)
        ft.enable_option(option="function-fork", instance=self.instance)
        ft.set_event_pid(pid=self.args.pids, instance=self.instance)
        ft.set_ftrace_pid(pid=self.args.pids, instance=self.instance)
        ft.tracing_ON(instance=self.instance)

        ft.wait(signals=['SIGUSR1', 'SIGINT'], pids=self.args.pids, time=self.duration)

        ft.tracing_OFF(instance=self.instance)
        ft.disable_option(option="event-fork", instance=self.instance)
        ft.disable_option(option="function-fork", instance=self.instance)
        ft.set_event_pid(pid=[], instance=self.instance)
        ft.set_ftrace_pid(pid=[], instance=self.instance)