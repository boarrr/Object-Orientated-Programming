# CMPU 2016 Object-Oriented Programming
# TU857-2
# 2024-25, Semester 1: Python with Sunder Ali Khowaja
# SunderAli.Khowaja@tudublin.ie
#
# Tutorial 2: Encapsulation.
# Managing data access.
#
# HOW TO USE THIS FILE:
# - Study each example
# - Copy sections of code into a separate file to try them out
# - This file should NOT be executed as one


# Example 1: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute can be accessed freely. This is the set-up of a
# class as you know it so far.

class Student:
    def __init__(self, name):
        self.name = name


ali = Student("Sunder Ali Khowaja")
print(ali.name)


# Example 2: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been hidden as a private variable using the
# Python private access modifier of the double underscore as a name prefix.

class Student:
    def __init__(self, name):
        self.__name = name


ali = Student("Sunder Ali Khowaja")
print(ali.__name) # this line causes an error, try writing on this
# variable. It will also cause an error.


# Example 3: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been marked as protected. Protected is like
# private, but for related classes. We are looking into inheritance next
# week. This example is here for completion. The protection is not enforced
# in Python.

class Student:
    def __init__(self, name):
        self._name = name


ali = Student("Sunder Ali Khowaja")
print(ali._name) # this still works. It's a flag to the programmer to not
# use this variable direclty. But Python does not enforce it. This is
# specific to Python. Other OOP languages interprete this idea differently.

# Let's stick with the private variable for a little while.
# Example 4: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been hidden as a private variable. We want
# to provide read access.
class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


ali = Student("Sunder Ali Khowaja")
print(ali.__name) # we already know that this does not work
print(ali.name) # notice how we can access this function as if it was an
# attribute

# Let's add some verfication to this, so that not everyone can access this
# variable at any time

# Example 5: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been hidden as a private variable. We want
# to provide read access but control access to specific situations.

import datetime


class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        today = datetime.date.today()
        # We restrict access to Mondays only in this example.
        # You could restrict it also to only specific user groups or
        # other business rules that make sense for your application.
        if today.weekday() == 0:  # Monday is 0, Tuesday is 1, and so on
            return self.__name
        else:
            return None


ali = Student("Sunder Ali Khowaja")
print(ali.__name) # we already know that this does not work
print(ali.name) # notice how we can access this function as if it was an
# attribute

# Let's see about writing
# Example 5: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been hidden as a private variable. We want
# to provide read and write access but control access to specific situations.

import datetime


class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        today = datetime.date.today()
        # We restrict access to Mondays only in this example.
        # You could restrict it also to only specific user groups or
        # other business rules that make sense for your application.
        if today.weekday() == 0:  # Monday is 0, Tuesday is 1, and so on
            return self.__name
        else:
            return None


ali = Student("Sunder Ali Khowaja")
ali.name = "Brian" # this line throws an error: object has no setter


# Example 6: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been hidden as a private variable. We want
# to provide read and write access but control access to specific situations.
# Here we add a setter.

import datetime


class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        today = datetime.date.today()
        # We restrict access to Mondays only in this example.
        # You could restrict it also to only specific user groups or
        # other business rules that make sense for your application.
        if today.weekday() == 6:  # Monday is 0, Tuesday is 1, and so on
            return self.__name
        else:
            return None

    @name.setter
    def name(self, value):
        self.__name = value


ali = Student("Sunder Ali Khowaja")
ali.name = "Brian"
print(ali.name)

# let's also do some checking up on the cases in which we allow this write
# access to happen.

# Example 7: A simple class, no behaviours, an attribute is set up in the
# init method. The attribute has been hidden as a private variable. We want
# to provide read and write access but control access to specific situations.
# Here we add a setter. We tightly control who's allowed to make changes.

import datetime
import getpass


class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        today = datetime.date.today()
        # We restrict access to Mondays only in this example.
        # You could restrict it also to only specific user groups or
        # other business rules that make sense for your application.
        if today.weekday() == 6:  # Monday is 0, Tuesday is 1, and so on
            return self.__name
        else:
            return None

    @name.setter
    def name(self, value):
        # Get the system's username
        system_username = getpass.getuser()

        if system_username == "skhowaja":
            self.__name = value
        else:
            print("You have not user rights to change attribute values.")


ali = Student("Sunder Ali Khowaja")
ali.name = "Brian"
#
# # if the correct user name has been given in the above statement, then this
# # will print Brian, otherwise it will print Bianca. Try it out!
print(ali.name)

