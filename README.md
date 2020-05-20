--------------------------------------------------------------------------------
Introduction
--------------------------------------------------------------------------------
This script should be executed before running benchmarks to determine the
current system settings and the execution enviroment.

Most information is gathered from sysfs/procfs files to reduce the dependecies.
Some information is only available through external tools (`likwid-*`, `nvidia-smi`,
`veosinfo`, `modules`) and some basic tools (`hostname`, `users`, ...).

--------------------------------------------------------------------------------
Differences between Shell and Python version
--------------------------------------------------------------------------------
The Shell version (`machine-state.sh`) executes some commands and just dumps the
output to stdout.

The Python version (`machine-state.py`) collects all data and outputs it in JSON
format. This version is currently under development.

--------------------------------------------------------------------------------
Checks
--------------------------------------------------------------------------------
- Shell version  (`machine-state.sh`)
    - Hostname, operating system and kernel version
    - Users that are logged into the system that might disturb the runs
    - CPUset
    - CPU and NUMA topology
    - CPU/Uncore frequency settings
    - Prefetchers
    - The current load of the system
    - OS settings (NUMA balancing, huge pages, ...)
    - Power contraints (RAPL limits)
    - Module system
    - Installed compilers and MPI implementations
    - Accelerator information (Nvidida GPUs and NEC Tsubasa)
    - Runtime enviroment
    - Dmidecode system configuration (if available)
    - Information about the benchmark (if cmd given as first argument)

- Python version (`machinestate.py`)
    - Hostname, operating system and kernel version
    - Users that are logged into the system that might disturb the runs
    - CPUset
    - CPU and NUMA topology
    - CPU/Uncore frequency settings
    - Prefetchers
    - The current load of the system
    - OS settings (NUMA balancing, huge pages, ...)
    - Power contraints (RAPL limits)
    - Module system
    - Installed compilers and MPI implementations
    - Runtime enviroment
    - Dmidecode system configuration (if available)
    - Information about the benchmark (if cmd is passed as cli argument)

--------------------------------------------------------------------------------
Usage (Python version)
--------------------------------------------------------------------------------
Getting usage help:
```
$ ./machinestate.py -h
usage: machinestate.py [-h] [-e] [executable]

Read system state and output as JSON document

positional arguments:
  executable      analyze executable (optional)

optional arguments:
  -h, --help      show this help message and exit
  -e, --extended  extended output
```

Gather data and print JSON

```
$ ./machinestate.py
{
    "HostInfo": {
        "Hostname": "testhost"
    },
    [...]
}
```

Gather extended data and print JSON

```
$ ./machinestate.py -e
{
    "HostInfo": {
        "Hostname": "testhost"
        "Domainname": "testdomain.de",
        "FQDN": "testhost.testdomain.de"
    },
    [...]
}
```

Gather data, include information about the executable on cmdline and print JSON

```
$ ./machinestate.py hostname
{
    "HostInfo": {
        "Hostname": "testhost"
    },
    [...]
    "ExecutableInfo": {
        "ExecutableInfo": {
            "Name": "hostname",
            "Abspath": "/bin/hostname",
            "Size": 18504
        },
        "LinkedLibraries": {
            "linux-vdso.so.1": null,
            "libc.so.6": "/lib/x86_64-linux-gnu/libc.so.6",
            "/lib64/ld-linux-x86-64.so.2": "/lib64/ld-linux-x86-64.so.2"
        }
    }
}
```