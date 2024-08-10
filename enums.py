from enum import Enum
import pydantic 

class Parameters(Enum):
    ENGINE_OIL_PRESSURE = 'ENGINE_OIL_PRESSURE'
    ENGINE_SPEED = 'ENGINE_SPEED'
    ENGINE_TEMPERATURE = 'ENGINE_TEMPERATURE'
    BRAKE_CONTROL = 'BRAKE_CONTROL'
    TRANSMISSION_PRESSURE = 'TRANSMISSION_PRESSURE'
    PEDAL_SENSOR = 'PEDAL_SENSOR'
    WATER_FUEL = 'WATER_FUEL'
    FUEL_LEVEL = 'FUEL_LEVEL'
    FUEL_PRESSURE = 'FUEL_PRESSURE'
    FUEL_TEMPERATURE = 'FUEL_TEMPERATURE'
    SYSTEM_VOLTAGE = 'SYSTEM_VOLTAGE'
    EXHAUST_GAS_TEMPERATURE = 'EXHAUST_GAS_TEMPERATURE'
    HYDRAULIC_PUMP_RATE = 'HYDRAULIC_PUMP_RATE' 
    AIR_FILTER_PRESSURE_DROP = 'AIR_FILTER_PRESSURE_DROP'

class Components(Enum):
    ENGINE = 'ENGINE'
    DRIVE = 'DRIVE'
    FUEL = 'FUEL'
    MISC = 'MISC'




parameters_enum = {component.name: component.value for component in Components}
probs = {
    'ENGINE_OIL_PRESSURE': 0.8,  # High
    'ENGINE_SPEED': 0.5,         # Medium
    'ENGINE_TEMPERATURE': 0.1,   # High
    'BRAKE_CONTROL': 0.5,        # Medium
    'TRANSMISSION_PRESSURE': 0.6, # Medium
    'PEDAL_SENSOR': 0.3,         # Low
    'WATER_FUEL': 0.7,           # High
    'FUEL_LEVEL': 0.3,           # Low
    'FUEL_PRESSURE': 0.3,        # Low
    'FUEL_TEMPERATURE': 0.8,     # High
    'SYSTEM_VOLTAGE': 0.8,       # High
    'EXHAUST_GAS_TEMPERATURE': 0.8, # High
    'HYDRAULIC_PUMP_RATE': 0.5,  # Medium
    'AIR_FILTER_PRESSURE_DROP': 0.5  # Medium
}