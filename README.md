# Assignment 01

[![Python 3.10.4](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-red.svg)](https://conventionalcommits.org)

## Assignment introduction

In this assignment we stride to achieve mutual exclusion, by way of implementing *Lamport's bakery algorithm*. Mutual exclusion is a fundamental concept in concurrent programming, that refers to the property of ensuring that only one process or thread can access a shared resource at a time. *Lamport's bakery algorithm* is one of few software solutions that improve the safety in the usage of shared resources among multiple threads by means of mutual exclusion.

## Mutual exclusion

To better understand mutual exclusion, let's assume a shared printer in an office as a shared resource. If multiple users try to print to the same printer simultaneously, the printer might not be able to handle all the requests at once. To prevent this, the printer uses a mutual exclusion technique, allowing only one user to print at a time.

### Necessary conditions for valid mutual exclusion solution

- Under no circumstances should two processes (threads) be within critical section simultaneously.

- A thread executing outside the critical section must not hinder other threads from entering it.

- If multiple threads are accessing the critical section,they must be allowed access within a finite amount of time.

- Processes must not assume anything about their timing or scheduling relative to each other when entering the critical section.

## Lamport's Bakery algorithm

Lamport's Bakery algorithm, proposed by Leslie Lamport in 1974, provides a fair and efficient solution for multiple threads or processes to access a shared resource or critical section of code. Let us explain fundamentals of this algorithm in following steps:

1. Each thread or process that wants to enter the critical section obtains a number (or ticket), by incrementing a global variable `num`, and then waits until its ticket number is the smallest.

2. The thread with the lowest number gets to access the critical section. If two threads have the same ticket number, the thread with the lower ID gets priority.

3. When a thread exits the critical section, it sets its ticket number to 0, indicating that it is no longer interested in accessing the critical section.

4. Other threads waiting to access the critical section continue to loop until their ticket number is the smallest. 
