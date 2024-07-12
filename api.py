from src.main import Simulation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
sim = Simulation()


class SimulationData(BaseModel):
    name: str


class PrimaryData(BaseModel):
    hash: str
    m: float


class OrbitalElementsData(BaseModel):
    hash: str
    m: float
    P: float
    e: float
    M: float
    a: Optional[float] = None
    inc: Optional[float] = None
    omega: Optional[float] = None
    Omega: Optional[float] = None


class BodyData(BaseModel):
    hash: str
    m: float
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    vx: Optional[float] = None
    vy: Optional[float] = None
    vz: Optional[float] = None


class BodyUpdateData(BaseModel):
    hash: str
    m: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    vx: Optional[float] = None
    vy: Optional[float] = None
    vz: Optional[float] = None


class TimeData(BaseModel):
    time: float


class TrajectoryData(BaseModel):
    start_time: float
    end_time: float
    time_step: float
    target: Optional[str] = None


@app.route('/')
def home():
    """
    Home route for the API. Returns a message indicating the API should be used via endpoints.

    Returns:
        str: A message indicating the API should be used via endpoints.
    """
    return 'This API should not be used in regular browser mode. Please use it as an API endpoint.'


@app.post('/create')
def create_route(data: SimulationData):
    global sim
    sim = Simulation(data.name)
    sim.save()
    return {"status": "success", "message": f"Simulation {data.name} created"}


@app.post('/load')
def load_route(data: SimulationData):
    global sim
    try:
        sim = Simulation.load(data.name)
        return {"status": "success", "message": f"Simulation {data.name} loaded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/add_primary')
def add_primary_route(data: PrimaryData):
    global sim
    try:
        sim.add_primary(**data.model_dump())
        sim.save()
        return {"status": "success", "message": f"{data.hash} added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/add_object')
def add_object_route(data: BodyData):
    global sim
    try:
        sim.add_object(**data.model_dump())
        sim.save()
        return {"status": "success", "message": f"{data.hash} added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/add_from_orbital_elements')
def add_from_orbital_elements_route(data: OrbitalElementsData):
    global sim
    try:
        sim.add_from_orbital_elements(**data.model_dump())
        sim.save()
        return {"status": "success", "message": f"{data.hash} added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/integrate')
def integrate_route(data: TimeData):
    global sim
    try:
        sim.integrate(data.time)
        sim.save()
        return {"status": "success", "message": f"Simulation {sim.name} integrated to {data.time}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/update_object')
def update_object_route(data: BodyUpdateData):
    global sim
    try:
        sim.update_object(**data.model_dump())
        sim.save()
        return {"status": "success", "message": f"{data.hash} updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/get_trajectory')
def get_trajectory_route(data: TrajectoryData):
    global sim
    try:
        result = sim.get_trajectory(**data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4242)
