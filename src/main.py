import os
import pickle
from typing import Any, Dict, Optional
import rebound
import numpy as np


class Simulation:
    def __init__(self, name: Optional[str] = None):
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

        if self.path:
            self.save()

    @property
    def time(self) -> float:
        return self._sim.t

    @property
    def particles(self) -> rebound.Particle:
        return self._sim.particles

    def copy(self) -> 'Simulation':
        copy_sim = Simulation(self.name)
        copy_sim._sim = self._sim.copy()
        copy_sim._particles = self._particles.copy()
        return copy_sim

    def save(self) -> None:
        with open(self.path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(name: str) -> 'Simulation':
        with open(os.path.join('simulations', name, 'sim.bin'), 'rb') as f:
            return pickle.load(f)

    def add_primary(self, m: float, hash: str) -> None:
        if self._sim.particles:
            raise ValueError('Primary already exists')

        primary_particle = rebound.Particle(m=m)
        primary_particle.hash = hash
        self._sim.add(primary_particle)
        self._particles[primary_particle.hash.value] = hash
        self._primary = primary_particle

    def add_object(self, m: float, hash: str, **kwargs: Any) -> None:
        particle = rebound.Particle(m=m, **kwargs)
        particle.hash = hash
        self._sim.add(particle)
        self._particles[particle.hash.value] = hash

    def add_from_orbital_elements(self, m: float, hash: str, **kwargs: Any) -> None:
        if self._primary is None:
            raise ValueError("Primary particle must be set before adding particles with orbital elements")

        particle = rebound.Particle(simulation=self._sim, primary=self._primary, m=m, **kwargs)
        particle.hash = hash
        self._sim.add(particle)
        self._particles[particle.hash.value] = hash

    def integrate(self, time: float) -> Dict[str, Any]:
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
