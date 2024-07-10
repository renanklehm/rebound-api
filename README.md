# Rebound API

This project is a RESTful API for the [REBOUND](https://github.com/hannorein/rebound) N-body simulation library. The goal of this API is easily integrate REBOUND into other applications without the need to integrate the C code directly.

## Features

- Create and save celestial simulations.
- Add primary and secondary bodies.
- Add bodies using orbital elements.
- Integrate simulations to a specific time.
- Retrieve trajectories over a specified period.

## Installation

### Prerequisites

- Python 3.12
- Conda
- Postman (for debugging API endpoints)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/renanklehm/rebound-api.git
    cd rebound-api
    ```

2. **Create and activate the Conda environment:**

    ```bash
    conda create --name rebound python=3.12
    conda activate rebound
    ```

3. **Install required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the API:**

    ```bash
    python api.py
    ```

    The API will be accessible at `http://127.0.0.1:4242`.

## Usage

### Postman Collection

To interact with the API you just need to make requests to the endpoints. A Postman collection is provided as a template to help you get started.

1. **Import the Postman collection:**

    - Open Postman.
    - Click on `Import` and select the `Rebound.postman_collection.json` file.

2. **Use the endpoints:**

    - `Create`: Create a new simulation.
    - `Load`: Load an existing simulation.
    - `Add primary body`: Add a primary body to the simulation.
    - `Add object`: Add a secondary body to the simulation.
    - `Add from orbital elements`: Add a body using orbital elements.
    - `Integrate`: Integrate the simulation to a specified time.
    - `Get trajectory`: Retrieve the trajectory of bodies over a specified period.

## Compilation

To compile the project using PyInstaller:

1. **Install PyInstaller:**

    ```bash
    pip install pyinstaller
    ```

2. **Create a .spec file:**

    The ```.spec``` is different for each project. To create a new one, run (Note that you will need to change the path to the the librebound binaries):

    ```bash
    pyinstaller api.py --onefile --name Rebound --icon icon.ico --add-binary PATH_TO_CONDA/envs/rebound/Lib/site-packages/librebound.cp312-###.pyd:. --add-data src/:. 
    ```

    The executable will be created in the `dist` directory. For future compilations, you can use the generated ```.spec``` by running:

    ```bash
    pyinstaller Rebound.spec
    ```

## License

REBOUND is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

REBOUND is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with REBOUND. If not, see http://www.gnu.org/licenses/.