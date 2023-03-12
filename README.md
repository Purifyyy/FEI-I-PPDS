# Assignment 03

[![Python 3.10.4](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-red.svg)](https://conventionalcommits.org)

## Assignment introduction

The *Dining Philosophers problem* is a classic computer science problem first introduced by Edsger W. Dijkstra in 1965. It is a thought experiment that challenges the concept of concurrency and resource allocation. The problem is presented as a scenario of five philosophers sitting around a table, where they must alternate between thinking and eating using forks.

## Specification of the problem

- There are 5 philosophers seated around a table (``NUM_PHILOSOPHERS``). Each philosopher has a fork on their left and right hand. There is only one fork between any two adjacent philosophers.

- The philosophers are thinking. After this activity, they become hungry and need to eat.

- To eat, the philosopher must pick up the fork on their left and right hand.

- Only one philosopher can hold a fork at a time.

- When a philosopher finishes eating, they put down both forks.

- We want to ensure that the philosophers do not die of hunger (prevent starvation).

- We want to prevent a situation where all philosophers are holding one fork and waiting indefinitely for the second fork held by their neighbor, creating a deadlock.

## Overview of important implementation parts

A class `Shared`, implementing the shared resources of philosophers simulation is defined. It consists of:

- A list of mutex locks `forks`, that represents shared forks on the table

Mutex lock `Mutex` and thread `Thread` classes used in our solution, are defined and implemented in the [fei.ppds](https://github.com/Programator2/ppds) python package.

For the philosopher threads, we implement target function with following signature `philosopher(i, shared)`, where `shared` is an instance of the `Shared` class, and `i` is a philosopher identifier.

In this function philosophers repeat their think-eat cycle for `NUM_RUNS` times. In each cycle, the philosopher begins with a thinking session, after which an attempt of raising forks occures. 

If a philosopher is **right-handed**, he first raises the fork on his right side. To demonstrate a situation of raising a fork on philosopher's right side, we use following code snippet:

```python
shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
```

After which he attempts to raise a fork on his left side. If he succeeds, he begins to eat. If the fork is not currently available, he waits. To demonstrate the raising of the fork on the left side of the philosopher, we use following code snippet:

```python
shared.forks[i].lock()
```

To ensure, no deadlock occures, **left-handed** philosopher raises forks in reverse order.

## Solutions comparison

Let's now compare our off-handed solution, to a solution that introduces a waiter. 

The waiter solution involves introducing a waiter or a resource manager who controls the allocation of forks. The philosophers need to ask the waiter for permission to use the forks, and the waiter ensures that no more than ``NUM_PHILOSOPHERS - 1`` philosophers can raise forks at the same time. After a philosopher has finished eating, they must inform the waiter that they are finished, which allows the waiter to grant permission to another philosopher.

#### Starvation and deadlock

Our **off-handed** philosopher solution is susceptible to the problem of starvation. This is because it does not guarantee that all philosophers will get to eat, especially if there is an imbalance between the number of left-handed and right-handed philosophers. In particular, two philosophers with the same handedness may keep picking up the same fork, preventing other philosophers from eating indefinitely.

On the other hand, the **waiter** solution provides a fairer and more balanced approach to the problem, and is less susceptible to starvation. By limiting the number of philosophers allowed to eat (raise forks) to four, it ensures that every philosopher gets a chance to eat, and prevents any one philosopher from monopolizing the forks for too long. However, it is worth noting that solution implementing a waiter may still be susceptible to starvation if the waiter himself is not implemented fairly. For example, if the waiter always grants permission to the same set of philosophers, then other philosophers may be starved of the opportunity to eat.

In summary, while both solutions can prevent deadlocks, the waiter solution provides a more fair and balanced approach that is less susceptible to starvation.

## Installation guide

In order to run our implementation of the *Dining philosophers problem*, it is recommended that a Python version 3.8, or higher is used. Additionally a [fei.ppds](https://github.com/Programator2/ppds) python package is required. The package can be installed using pip:

```
pip install --upgrade fei.ppds
```
