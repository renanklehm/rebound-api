import os
import pickle
from typing import Any, Dict, Optional
import rebound
import numpy as np


class Simulation:
    """
    Class representing a celestial simulation using the REBOUND library.

    Attributes:
        name (str): The name of the simulation, used for saving and loading.
        path (str): The file path where the simulation is saved.
        _sim (rebound.Simulation): The REBOUND simulation instance.
        _particles (dict): A dictionary mapping particle hashes to their names.
        _primary (rebound.Particle): The primary particle in the simulation.
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initialize the Simulation object.

        Args:
            name (Optional[str]): The name of the simulation. If provided, a directory
                                  will be created for saving the simulation.
        """
        if name:
            os.makedirs(os.path.join('simulations', name), exist_ok=True)
            self.name = name
            self.path = os.path.join('simulations', name, 'sim.bin')
        else:
            self.name = ''
            self.path = ''

        self._sim = rebound.Simulation()
        self._sim.units = ('s', 'm', 'kg')
        self._particles = {}
        self._primary = None

    @property
    def time(self) -> float:
        """Get the current simulation time."""
        return self._sim.t

    @property
    def particles(self) -> rebound.Particle:
        """Get the particles in the simulation."""
        return self._sim.particles

    def copy(self) -> 'Simulation':
        """
        Create a copy of the simulation.

        Returns:
            Simulation: A copy of the current simulation.
        """
        copy_sim = Simulation(self.name)
        copy_sim._sim = self._sim.copy()
        copy_sim._particles = self._particles.copy()
        return copy_sim

    def save(self) -> None:
        """Save the simulation to a file."""
        with open(self.path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(name: str) -> 'Simulation':
        """
        Load a simulation from a file.

        Args:
            name (str): The name of the simulation to load.

        Returns:
            Simulation: The loaded simulation object.
        """
        with open(os.path.join('simulations', name, 'sim.bin'), 'rb') as f:
            return pickle.load(f)

    def add_primary(self, m: float, hash: str) -> None:
        """
        Add the primary particle to the simulation.

        Args:
            m (float): The mass of the primary particle.
            hash (str): The hash identifier for the primary particle.

        Raises:
            ValueError: If a primary particle already exists.
        """
        if self._sim.particles:
            raise ValueError('Primary already exists')

        primary_particle = rebound.Particle(m=m)
        primary_particle.hash = hash
        self._sim.add(primary_particle)
        self._particles[primary_particle.hash.value] = hash
        self._primary = primary_particle

    def add_object(self, m: float, hash: str, **kwargs: Any) -> None:
        """
        Add an object to the simulation.

        Args:
            m (float): The mass of the object.
            hash (str): The hash identifier for the object.
            **kwargs: Additional keyword arguments for particle properties.
        """
        particle = rebound.Particle(m=m, **kwargs)
        particle.hash = hash
        self._sim.add(particle)
        self._particles[particle.hash.value] = hash

    def add_from_orbital_elements(self, m: float, hash: str, **kwargs: Any) -> None:
        """
        Add an object to the simulation using orbital elements.

        Args:
            m (float): The mass of the object.
            hash (str): The hash identifier for the object.
            **kwargs: Additional keyword arguments for orbital elements.

        Raises:
            ValueError: If the primary particle is not set.
        """
        if self._primary is None:
            raise ValueError("Primary particle must be set before adding particles with orbital elements")

        particle = rebound.Particle(simulation=self._sim, primary=self._primary, m=m, **kwargs)
        particle.hash = hash
        self._sim.add(particle)
        self._particles[particle.hash.value] = hash

    def update_object(self, hash: str, **kwargs: Any) -> None:
        """
        Update the properties of an object in the simulation.

        Args:
            hash (str): The hash identifier for the object.
            **kwargs: Additional keyword arguments for particle properties.
        """
        particle = self._sim.particles[hash]
        for key, value in kwargs.items():
            setattr(particle, key, value)

    def integrate(self, time: float) -> Dict[str, Any]:
        """
        Integrate the simulation to a specified time.

        Args:
            time (float): The time to integrate to.

        Returns:
            Dict[str, Any]: A dictionary containing the positions and velocities of particles at the given time.
        """
        self._sim.integrate(time)
        result = {}
        for particle in self._sim.particles:
            name = self._particles[particle.hash.value]
            result[name] = {
                self.time: {
                    'position': particle.xyz,
                    'velocity': particle.vxyz
                }
            }
        return result

    def get_prediction(self, time: float, target: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the predicted state of particles at a future time.

        Args:
            time (float): The time to predict to.
            target (Optional[str]): The hash of the target particle to predict. If None, all particles are predicted.

        Returns:
            Dict[str, Any]: A dictionary containing the predicted positions and velocities of particles at the given time.
        """
        prediction_sim = self.copy()
        prediction_sim.integrate(time)
        result = {}

        if target:
            target_particle = prediction_sim.particles[target]
            result[target] = {
                prediction_sim.time: {
                    'position': target_particle.xyz,
                    'velocity': target_particle.vxyz
                }
            }
        else:
            for particle in prediction_sim.particles:
                name = prediction_sim._particles[particle.hash.value]
                result[name] = {
                    prediction_sim.time: {
                        'position': particle.xyz,
                        'velocity': particle.vxyz
                    }
                }
        return result

    def get_trajectory(self, end_time: float, time_step: float, target: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the trajectory of particles over a time period.

        Args:
            end_time (float): The end time of the trajectory.
            time_step (float): The time step between points in the trajectory.
            target (Optional[str]): The hash of the target particle to get the trajectory for. If None, all particles are included.

        Returns:
            Dict[str, Any]: A dictionary containing the trajectories of particles over the specified time period.
        """
        trajectory_sim = self.copy()
        result = {}

        for current_time in np.arange(trajectory_sim.time, end_time, time_step):
            trajectory_sim.integrate(current_time)

            if target:
                target_particle = trajectory_sim.particles[target]
                if target not in result:
                    result[target] = {}
                result[target][trajectory_sim.time] = {
                    'position': target_particle.xyz,
                    'velocity': target_particle.vxyz
                }
            else:
                for particle in trajectory_sim.particles:
                    name = trajectory_sim._particles[particle.hash.value]
                    if name not in result:
                        result[name] = {}
                    result[name][trajectory_sim.time] = {
                        'position': particle.xyz,
                        'velocity': particle.vxyz
                    }
        return result
