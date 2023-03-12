# Assignment 03

[![Python 3.10.4](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-red.svg)](https://conventionalcommits.org)

## Assignment introduction



The *Dining Philosophers problem* is a classic computer science problem first introduced by Edsger W. Dijkstra in 1965. It is a thought experiment that challenges the concept of concurrency and resource allocation. The problem is presented as a scenario of five philosophers sitting around a table, where they must alternate between thinking and eating using forks.

## Specification of the problem

- There are 5 philosophers seated around a table. Each philosopher has a fork on their left and right hand. There is only one fork between any two adjacent philosophers.

- The philosophers are thinking. After this activity, they become hungry and need to eat.

- To eat, the philosopher must pick up the fork on their left and right hand.

- Only one philosopher can hold a fork at a time.

- When a philosopher finishes eating, they put down both forks.

- We want to ensure that the philosophers do not die of hunger (prevent starvation).

- We want to prevent a situation where all philosophers are holding one fork and waiting indefinitely for the second fork held by their neighbor, creating a deadlock.
