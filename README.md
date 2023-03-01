# Assignment 02

[![Python 3.10.4](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-red.svg)](https://conventionalcommits.org)

## Assignment introduction

In this assignment we attempt to implement a classic synchronization problem in concurrent programming, called the *Sleeping Barber Problem*. It involves a barber who runs a barbershop with multiple chairs for customers to sit in and wait to be served. If there are no customers in the shop, the barber goes to sleep. When a customer arrives, they either wake the barber up, or sit in the waiting room chair if the barber is busy cutting someone else's hair. The problem is to coordinate the barber and the customers in such a way that no customer is turned away (unless there is no space in the waiting room) and the barber is not overworked.

## Specification of the problem

The task at hand, is to manage the coordination between clients and the barber.

**The barbershop consists of 2 rooms**:

- Waiting room for ``N`` clients
- The barber's room

**If there are no clients, the barber sleeps**.

**If a client enters**:

- And all the chairs are occupied, he leaves
- And the barber is busy, but there is an available chair, he sits and waits
- And the barber sleeps, the client wakes him up and sits to wait

## Overview of important implementation parts

A class ``Shared``, implementing the shared resources of the barber shop simulation is defined. It consists of:

- A muted lock ``mutex``, that assures mutual exclusion between customers on entry, and exit of the waiting room

- An integer ``waiting_room``, keeping a track of the occupation level of the waiting room

- A semaphore ``customer``, for a way to signal the barber upon customer's arrival 

- A semaphore `barber`, that signals customer, when the barber is ready to cut hair

- A semaphore ``customer_done``, to let the barber know that customer's haircut is done

- A semaphore ``barber_done``, so barber can signal the customer, that the hair cutting is finished

Mutex lock ``Mutex``, semaphore ``Semaphore``, and thread ``Thread`` classes used in our implementation, are defined and implemented in the [fei.ppds](https://github.com/Programator2/ppds) python package.

For both the barber thread and the customer threads, we implement target functions with following signatures. `customer(i, shared)`, `barber(shared)`, where `shared` is an instance of the `Shared` class, and `i` is a customer identifier.

Before incrememting or decrementing the ``waiting_room`` variable (indicating customer's entry and exit of the waiting area), the customer thread function must acquire ``mutex`` lock. After performing this operation, the function releases it.

### Rendezvous points

To achieve a simulation where barber is woken up by a customer, prepares for hair cutting and subsequently signals the customer he's ready to cut hair, we use a pair of defined semaphores, `customer` and `barber`. To demonstrate this situation from the customer function perspective, we will use following code snippet:

```python
shared.customer.signal() # wake the barber up
shared.barber.wait()     # wait for barber to get ready
# get a haircut
```

 Alternatively, from the barber function perspective:

```python
shared.customer.wait() # sleep while waiting for customer
shared.barber.signal() # signal the ready state for cutting hair
# cut hair
```

These code snippets, display important synchronization point in the code, known as rendezvous point.

The other rendezvous point occurs when the customer waits for the hair cutting to be finished. Barber must signal the customer, that the hair cutting is concluded, subsequently the barber has to wait for the customer to signal, that the haircut is done. In this case we use the pair of semaphores ``customer_done`` and ``barber_done``. Rendezvous point from the customer function perspective:

```python
# get a haircut
shared.barber_done.wait()       # wait for barber to finish cutting hair
shared.customer_done.signal()   # customer is done getting a haircut
```

Lastly, from the perspective of the barber function:

```python
# cut hair
shared.barber_done.signal()  # barber is done cutting the hair
shared.customer_done.wait()  # wait for customer to be finished getting a haircut
```

## Sample run of the program

The following figure demonstrates one of many possible correct scenarios of our implementation of the *Sleeping Barber Problem*.

![ScreenShot](https://i.imgur.com/vIckPA7_d.webp?maxwidth=760&fidelity=grand)

## Installation guide

In order to run our implementation of the *Sleeping Barber Problem*, it is recommended that a Python version 3.8, or higher is used. Additionally a [fei.ppds](https://github.com/Programator2/ppds) python package is required. The package can be installed using pip: 

```
pip install --upgrade fei.ppds
```
