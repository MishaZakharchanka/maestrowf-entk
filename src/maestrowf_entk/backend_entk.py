import json
from typing import List
from collections import deque
import radical.entk as re
import radical.pilot as rp

class Converter:

    _workflow = {'tasks':{}, 'resource':{}}

    max_cores = 0
    max_gpus = 0

    def __init__(self, exec_graph):
        self._dag = exec_graph

    def bfs(self, src):
        queue = deque([(src, -1)])
        path = [src]
        return_thingy = {}
        level = 0

        while queue:
            root, level = queue.popleft()
            return_thingy.update({root: level})
            for node in self._dag.adjacency_table[root]:
                if node in path:
                    continue

                path.append(node)
                queue.append((node, level + 1))

        return return_thingy, level


    def process(self, store:bool):
        stage, highest_stage = self.bfs("_source")

        # Create dict for stages before populating
        for i in range(highest_stage + 1):
            self._workflow['tasks'].update({i: {}})

        for key in self._dag.values.keys():
            # Check that we are not on the root node
            if not self._dag.values[key]:
                continue

            # get rid of source (the root of the Graph from maestro) dependancy
            dep_list = list(self._dag._dependencies[key])
            if "_source" in dep_list:
                dep_list.remove("_source")

            task = {
                'inputs' : self._dag.values[key].params,
                'exec' : self._dag.values[key].step.run['cmd'],
                'depends_on' : dep_list,
                'cores' : 1,
                'gpus' : 0,
                'walltime' : 1
            }

            if self._dag.values[key].step.run['procs']:
                task['cores'] = int(self._dag.values[key].step.run['procs'])
            if self._dag.values[key].step.run['gpus']:
                task['gpus'] = int(self._dag.values[key].step.run['gpus'])
            if self._dag.values[key].step.run['walltime']:
                task['walltime'] = int(self._dag.values[key].step.run['walltime'])

            self._workflow['tasks'][stage[key]].update({self._dag.values[key].step.real_name : task})

            if "host" not in self._dag._adapter:
                self._dag._adapter["host"] = "local"

        max_cores_per_stage = 0
        max_gpus_per_stage = 0
        max_walltime_per_stage = 0
        total_walltime = 0
        for stage in self._workflow['tasks']:
            cores_per_stage = 0
            gpus_per_stage = 0
            walltime_per_stage = 0
            for task in self._workflow['tasks'][stage].values():
                if task['cores']:
                    cores_per_stage += task['cores']
                if task['gpus']:
                    gpus_per_stage += task['gpus']
                if task['walltime'] > walltime_per_stage:
                    walltime_per_stage = task['walltime']
            if cores_per_stage > max_cores_per_stage:
                max_cores_per_stage = cores_per_stage
            if gpus_per_stage > max_gpus_per_stage:
                max_gpus_per_stage = gpus_per_stage
            if walltime_per_stage > max_walltime_per_stage: # This is just to calculate total Walltime
                max_walltime_per_stage = walltime_per_stage   # do not need this in resource list
            total_walltime += walltime_per_stage

        resource = {
          'cores' : max_cores_per_stage, # pick maximum from tasks
          'gpus' : max_gpus_per_stage, # Same thing as above
          'walltime' : total_walltime, # add all walltimes together
          'host' : self._dag._adapter["host"], # Host and batch should be the same machine
          'batch' : self._dag._adapter["type"]
        }

        self._workflow['resource'].update(resource)

        # If the entk option that includes store is used, then dump data
        if store:
            with open('workflow.json', 'w') as fp:
                json.dump(self._workflow, fp, indent=2)

        radical_stages = []

        for i in range(highest_stage + 1):
            radical_stages.append(re.Stage())

            for x in self._workflow['tasks'][i]:
                exec_string = self._workflow['tasks'][i][x]['exec'].replace('\n', '')

                task = re.Task()
                task.executable = exec_string
                if self._workflow['tasks'][i][x]['cores']:
                    task.cpu_reqs = {'cpu_threads' : self._workflow['tasks'][i][x]['cores']} # this should be threads
                if self._workflow['tasks'][i][x]['gpus']:
                    task.gpu_reqs = {'gpu_processes' : self._workflow['tasks'][i][x]['gpus']}
                # Will need to add per test walltime (timeout) when Mikhail adds it to entk

                radical_stages[-1].add_tasks(task)

        platform_ids = get_platform_ids(self._workflow['resource']['host'])
        radical_resource = 'local.localhost_test' if not platform_ids else platform_ids[0]

        my_pipeline = re.Pipeline()
        my_pipeline.add_stages(radical_stages)

        appman = re.AppManager()
        appman.resource_desc = {
            'resource' : radical_resource,
            'walltime' : total_walltime,
            'cpus' : max_cores_per_stage,
            'gpus' : max_gpus_per_stage
        }

        appman.workflow = [my_pipeline]
        appman.run()


def get_platform_ids(hostname:str) -> List[str]:

    platform_cfgs = rp.utils.get_resource_configs()
    facilities = list(platform_cfgs)
    for skip_facility in ['debug', 'local']:
        facilities.remove(skip_facility)
    output = []
    for facility in facilities:
        for platform in platform_cfgs[facility]:
            if platform.split('_')[0] in hostname:
                output.append('%s.%s' % (facility, platform))
        if output:
            output.sort()
            break
    return output
