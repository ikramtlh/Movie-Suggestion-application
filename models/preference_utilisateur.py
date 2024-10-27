import collections.abc

collections.Callable = collections.abc.Callable
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet

from experta import *


# Define the fact and rules for movie recommendations
class PreferenceUtilisateur(Fact):
    genre_preferee = Field(str)
    note_souhaitee = Field(float)
    language_preferee = Field(str)
    date_preferee = Field(int)
