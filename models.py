"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        # self.designation = info['pdes'] if info['pdes'] != '' else None
        # self.name = info['name'] if info['name'] != '' else None
        # self.diameter = float(info['diameter']) if info['diameter'] != '' else float('nan')
        # self.hazardous = True if info['pha'] == 'Y' else False

        for key, value in info.items():
            if key.lower() == 'pdes':
                try:
                    self.designation = str(value)
                except ValueError:
                    print(f'{key} is not a string.')
            elif key.lower() == 'name':
                if len(value) != 0:
                    try:
                        self.name = str(value)
                    except ValueError:
                        print(f"{key} is not a string.")
                else:
                    self.name = None
            elif key.lower() == 'diameter':
                if len(value) != 0:
                    try:
                        self.diameter = float(value)
                    except ValueError:
                        print(f'{key} is not a float.')
                else:
                    self.diameter = float('nan')
            elif key.lower() == 'pha':
                try:
                    self.hazardous = str(value)
                    if self.hazardous.lower() == 'y':
                        self.hazardous = True
                    else:
                        self.hazardous = False
                except ValueError:
                    print(f'{key} is not a string.')

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def append_approach(self, approach):
        """ To add info of a close approach of a NEO
         :param approach object
         :return
         """

        if type(approach) == CloseApproach:
            self.approaches.append(approach)

    def serialize(self):
        return {'designation': self.designation, 'name': self.name, 'diameter_km': self.diameter,
                'potentially_hazardous': self.hazardous}

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # Use self.designation and self.name to build a fullname for this object.
        if self.name is not None:
            return f'{self.designation} {self.name}'
        else:
            return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        if self.hazardous:
            return f"A NearEarthObject of name {self.name}, short for {self.designation}," \
                f" has a diameter of {self.diameter:.3f}km and is potentially hazardous.\n"
        else:
            return f"A NearEarthObject of name {self.name}, short for {self.designation}," \
                   f" has a diameter of {self.diameter:.3f}km and is not potentially hazardous.\n"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `CloseApproach`.
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        for key, value in info.items():
            if key.lower() == 'des':
                try:
                    self._designation = str(value)
                except ValueError:
                    print(f'{key} is not a string.')
            elif key.lower() == 'cd':
                try:
                    self.time = str(value)
                    self.time = cd_to_datetime(self.time)
                except ValueError:
                    print(f'{key} is not a string.')
            elif key.lower() == 'dist':
                try:
                    self.distance = float(value)
                except ValueError:
                    print(f'{key} is not a float.')
            elif key.lower() == 'v_rel':
                try:
                    self.velocity = float(value)
                except ValueError:
                    print(f'{key} is not a float.')

        # Create an attribute for the referenced NEO, originally None.
        self.neo = self._designation

    def serialize(self):
        return {'datetime_utc': datetime_to_str(self.time), 'distance_au': self.distance,
                'velocity_km_s': self.velocity}

    @property
    def designation(self):
        """ Return a representation of the designation of the NEO
        corresponding to this CloseApproach. """
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        date_time = datetime_to_str(self.time)
        # Use self.designation and self.name to build a fullname for this object.
        return date_time

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"On {self.time}, {self.neo.fullname} approaches Earth at a distance of {self.distance:.2f} au and " \
               f"a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
