/**
 * RoamK - OpenRoam Data Store
 * Similar to Signal K for marine vessels, RoamK provides a unified
 * data model for all vehicle systems.
 */

import { writable, derived, type Readable } from 'svelte/store';

// Type definitions for RoamK data model
export interface Location {
	latitude: number;
	longitude: number;
	altitude?: number;
	speed?: number;
	heading?: number;
	satellites?: number;
}

export interface BatteryBank {
	voltage: number;
	current: number;
	soc: number;
	temp?: number;
	capacity_ah?: number;
}

export interface PowerState {
	batteries: {
		house?: BatteryBank;
		chassis?: BatteryBank;
		aux?: BatteryBank;
	};
	solar: {
		voltage: number;
		current: number;
		watts: number;
		daily_wh: number;
		lifetime_kwh?: number;
	};
	shore: {
		connected: boolean;
		voltage: number;
		amps: number;
	};
	alternator: {
		charging: boolean;
		amps: number;
	};
}

export interface TankLevel {
	level: number;
	gallons?: number;
	capacity?: number;
}

export interface TanksState {
	fresh: TankLevel;
	grey: TankLevel;
	black: TankLevel;
	propane: TankLevel & { pounds?: number };
	fuel: TankLevel & { range_miles?: number };
}

export interface ClimateZone {
	temperature: number;
	setpoint?: number;
	humidity?: number;
}

export interface ClimateState {
	interior: { temperature: number; humidity: number };
	exterior: { temperature: number; humidity: number };
	zones: Record<string, ClimateZone>;
	hvac: {
		mode: 'heat' | 'cool' | 'auto' | 'off';
		running: boolean;
		fan_speed: number;
	};
}

export interface EngineState {
	rpm: number;
	coolant_temp: number;
	oil_temp: number;
	oil_pressure: number;
	trans_temp: number;
	throttle: number;
	load: number;
	fuel_rate: number;
	mpg_instant: number;
	mpg_average: number;
	dtc_codes: string[];
	check_engine: boolean;
}

export interface SafetyState {
	smoke: { status: 'ok' | 'warning' | 'alarm' };
	co: { ppm: number; status: 'ok' | 'warning' | 'alarm' };
	propane: { ppm: number; status: 'ok' | 'warning' | 'alarm' };
	doors: Record<string, 'open' | 'closed'>;
	alarm: { armed: boolean; triggered: boolean };
}

export interface VehicleState {
	location: Location;
	speed: number;
	heading: number;
	odometer: number;
	leveling?: {
		pitch: number;
		roll: number;
		state: 'leveling' | 'level' | 'travel';
	};
}

export interface MaintenanceItem {
	service: string;
	due_miles?: number;
	due_date?: string;
}

export interface MaintenanceState {
	oil_life: number;
	next_oil_miles: number;
	tire_rotation_due: boolean;
	upcoming: MaintenanceItem[];
}

export interface SystemNode {
	name: string;
	online: boolean;
	cpu: number;
	memory: number;
	temp: number;
	disk: number;
}

export interface NetworkState {
	wifi_clients: number;
	cellular_signal: number;
	carrier: string;
	data_used_gb: number;
	starlink?: {
		connected: boolean;
		speed_mbps: number;
		obstructions: number;
	};
}

// Complete RoamK state
export interface RoamKState {
	vehicle: VehicleState;
	power: PowerState;
	tanks: TanksState;
	climate: ClimateState;
	engine: EngineState;
	safety: SafetyState;
	maintenance: MaintenanceState;
	network: NetworkState;
	system: {
		nodes: SystemNode[];
	};
	lastUpdate: number;
}

// Default initial state - populated by MQTT data from hardware
const initialState: RoamKState = {
	vehicle: {
		location: { latitude: 0, longitude: 0 },
		speed: 0,
		heading: 0,
		odometer: 0
	},
	power: {
		batteries: {
			house: { voltage: 0, current: 0, soc: 0 },
			chassis: { voltage: 0, current: 0, soc: 0 }
		},
		solar: { voltage: 0, current: 0, watts: 0, daily_wh: 0 },
		shore: { connected: false, voltage: 0, amps: 0 },
		alternator: { charging: false, amps: 0 }
	},
	tanks: {
		fresh: { level: 0 },
		grey: { level: 0 },
		black: { level: 0 },
		propane: { level: 0 },
		fuel: { level: 0 }
	},
	climate: {
		interior: { temperature: 0, humidity: 0 },
		exterior: { temperature: 0, humidity: 0 },
		zones: {},
		hvac: { mode: 'off', running: false, fan_speed: 0 }
	},
	engine: {
		rpm: 0,
		coolant_temp: 0,
		oil_temp: 0,
		oil_pressure: 0,
		trans_temp: 0,
		throttle: 0,
		load: 0,
		fuel_rate: 0,
		mpg_instant: 0,
		mpg_average: 0,
		dtc_codes: [],
		check_engine: false
	},
	safety: {
		smoke: { status: 'ok' },
		co: { ppm: 0, status: 'ok' },
		propane: { ppm: 0, status: 'ok' },
		doors: {},
		alarm: { armed: false, triggered: false }
	},
	maintenance: {
		oil_life: 100,
		next_oil_miles: 5000,
		tire_rotation_due: false,
		upcoming: []
	},
	network: {
		wifi_clients: 0,
		cellular_signal: 0,
		carrier: '',
		data_used_gb: 0
	},
	system: {
		nodes: []
	},
	lastUpdate: Date.now()
};

// Create the main store
function createRoamKStore() {
	const { subscribe, set, update } = writable<RoamKState>(initialState);

	return {
		subscribe,
		set,
		update,

		// Update a specific path in the state
		updatePath: (path: string, value: unknown) => {
			update((state) => {
				const parts = path.split('.');
				let current: Record<string, unknown> = state as unknown as Record<string, unknown>;

				for (let i = 0; i < parts.length - 1; i++) {
					if (!(parts[i] in current)) {
						current[parts[i]] = {};
					}
					current = current[parts[i]] as Record<string, unknown>;
				}

				current[parts[parts.length - 1]] = value;
				state.lastUpdate = Date.now();
				return state;
			});
		},

		// Reset to initial state
		reset: () => set(initialState)
	};
}

// Export the main store
export const roamk = createRoamKStore();

// Derived stores for specific sections
export const vehicle: Readable<VehicleState> = derived(roamk, ($roamk) => $roamk.vehicle);
export const power: Readable<PowerState> = derived(roamk, ($roamk) => $roamk.power);
export const tanks: Readable<TanksState> = derived(roamk, ($roamk) => $roamk.tanks);
export const climate: Readable<ClimateState> = derived(roamk, ($roamk) => $roamk.climate);
export const engine: Readable<EngineState> = derived(roamk, ($roamk) => $roamk.engine);
export const safety: Readable<SafetyState> = derived(roamk, ($roamk) => $roamk.safety);
export const maintenance: Readable<MaintenanceState> = derived(roamk, ($roamk) => $roamk.maintenance);
export const network: Readable<NetworkState> = derived(roamk, ($roamk) => $roamk.network);

// Connection status
export const connected = writable(false);
