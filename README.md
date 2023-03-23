# Assignment 04

[![Python 3.10.4](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-red.svg)](https://conventionalcommits.org)

## Assignment introduction

A concurrency and resource allocation problem involving a group of **savages** who must share a communal pot of food. The savages in Equatorial Guinea are a very social and sophisticated type of people. Not only do they eat together every day, but they also have skilled cooks among them who prepare excellent zebra goulash. However, they need a reliable system in which to communicate all the actions related to the communal feast.

## Specification of the problem

- The savages always start eating together. The last savage to arrive signals to everyone that they are all present and can begin feasting.

- Each savage takes their portion from the pot until it is empty.

- The savage who notices that the pot is empty alerts the cooks to prepare more.

- The savages wait for the cooks to refill the pot.

- The cook always prepares one serving and adds it to the pot.

- Once the pot is full, the savages continue feasting.

- The whole process repeats in an endless cycle.

## Overview of important implementation parts

Global variables `H`, `D` and `K` define the maximum number of portions in a pot, number of savages and number of cooks, respectively.

A class `Shared`, implementing the shared resources of savages and cooks is defined. It consists of:

- An integer `pot`, keeping a track of number of portions in the pot
- A mutex lock `savage_mutex`, that assures mutual exclusion between savages, when taking a portion from the pot
- A mutex lock `cook_mutex`, ensuring mutual exclusion among cooks while adding portions to the pot
- A binary semaphore `full_pot`, to signal the savages upon fully refilling the empty pot
- An event `empty_pot`, for savages to alert the cooks, that a pot refill is necessary

Additionally the shared class also defines components for the savage barrier:

- An interger `barrier_count`, to keep track of savage count going through tourniquet

- A mutex lock `barrier_mutex`, to ensure mutual exclusion when going through tourniquet

- A semaphore `turnstile1`, that acts as entrance tourniquet

- A semaphore `turnstile2`, as exit tourniquet

Mutex lock `Mutex`, semaphore `Semaphore`, an event `Event` and thread `Thread` classes used in our implementation, are defined and implemented in the [fei.ppds](https://github.com/Programator2/ppds) python package.

For both the savage thread and the cook thread, we implement target functions with following signatures. `savage(i, shared)`, `cook(i, shared)`, where `shared` is an instance of the `Shared` class, and `i` is a savage and cook identifier respectively.

#### Barrier

To ensure that the savages always begin the feast together, our implementation uses a barrier. A barrier is a synchronization pattern defines a point that a thread is allowed to go past only when all threads have reached it [[1]](#1). The components that compose a barrier in our implementation, were mentioned above. The following code snippet represents the barrier:

```python
shared.barrier_mutex.lock()
shared.barrier_count += 1
if shared.barrier_count == D:
    shared.turnstile1.signal(D)
shared.barrier_mutex.unlock()
shared.turnstile1.wait()
# let the feast begin
```

Considering our implementation runs in an endless cycle, we must preserve its reusebility. We do that after each cycle, using following code snippet:

```python
shared.barrier_mutex.lock()
shared.barrier_count -= 1
if shared.barrier_count == 0:
    shared.turnstile2.signal(D)
shared.barrier_mutex.unlock()
shared.turnstile2.wait()
```

#### Savage

Once the savages get through the barrier, one by one they acquire a `savage_lock`, and check whether there is any food left in the pot. The savage that finds out there isn't, signals the cooks (using the `empty_pot` event) to refill the pot, and waits (on the `full_pot` semaphore) until they do so. If there already is food inside the pot, or the cooks singnaled that the pot has been refilled, the savage takes a portion and releases the `savage_lock`. This process can be seen in the following code snippet:

```python
shared.savage_mutex.lock()
if shared.pot == 0:
    shared.empty_pot.signal()
    shared.full_pot.wait()
get_portion(i, shared)
shared.savage_mutex.unlock()
```

#### Cook

Cooks must wait (using `empty_poy` event) until savages inform them about an empty pot. Once they do, one by one, cooks check whether they've fully refilled the pot. If not a cook may add the cooked portion to the pot. Once a cook realizes that the pot is fully refilled, they set the ``empty_pot`` event state to waiting and inform the savages, that the feast can be resumed (with ``full_pot`` singal). This process is being performed under the `cook_mutex` lock, and can be seen on following code snippet:

```python
# cook a portion
shared.cook_mutex.lock()
shared.empty_pot.wait()
if shared.pot == H:
    shared.empty_pot.clear()
    shared.full_pot.signal()
    shared.cook_mutex.unlock()
    continue
put_portion(i, shared)
shared.cook_mutex.unlock()
```

## Sample run of the program

The following figure demonstrates one of many possible correct scenarios of our implementation, using 5 portions per pot (`H = 5`), 3 savages (`D = 3`) and 4 cooks (`K = 4`).

<img src="https://i.imgur.com/Z15J3uQ.png" title="implementation run example" alt="sampleRunScreenshot">

## Installation guide

In order to run our implementation of the sophisticated savages feast, it is recommended that a Python version 3.8, or higher is used. Additionally a [fei.ppds](https://github.com/Programator2/ppds) python package is required. The package can be installed using pip:

```
pip install --upgrade fei.ppds
```

## References

<a id="1">[1]</a> 
Solihin, Yan. (2015). 
Fundamentals of Parallel Multicore Architecture. 10.1201/b20200. 