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

// Default initial state with demo data for screenshots
const initialState: RoamKState = {
	vehicle: {
		location: { latitude: 35.6762, longitude: -105.9636, altitude: 2134 },
		speed: 0,
		heading: 225,
		odometer: 45230
	},
	power: {
		batteries: {
			house: { voltage: 13.2, current: -5.5, soc: 85, temp: 75, capacity_ah: 400 },
			chassis: { voltage: 12.8, current: 0, soc: 98 }
		},
		solar: { voltage: 38.5, current: 11.7, watts: 450, daily_wh: 2850, lifetime_kwh: 1250.5 },
		shore: { connected: false, voltage: 0, amps: 0 },
		alternator: { charging: false, amps: 0 }
	},
	tanks: {
		fresh: { level: 72, gallons: 29, capacity: 40 },
		grey: { level: 35, gallons: 14, capacity: 40 },
		black: { level: 18, gallons: 7, capacity: 40 },
		propane: { level: 65, pounds: 19.5 },
		fuel: { level: 58, gallons: 29, capacity: 50, range_miles: 290 }
	},
	climate: {
		interior: { temperature: 72, humidity: 45 },
		exterior: { temperature: 85, humidity: 28 },
		zones: {
			living: { temperature: 72, setpoint: 70 },
			bedroom: { temperature: 70, setpoint: 68 }
		},
		hvac: { mode: 'cool', running: true, fan_speed: 2 }
	},
	engine: {
		rpm: 0,
		coolant_temp: 185,
		oil_temp: 195,
		oil_pressure: 42,
		trans_temp: 165,
		throttle: 0,
		load: 0,
		fuel_rate: 0,
		mpg_instant: 0,
		mpg_average: 10.2,
		dtc_codes: [],
		check_engine: false
	},
	safety: {
		smoke: { status: 'ok' },
		co: { ppm: 0, status: 'ok' },
		propane: { ppm: 0, status: 'ok' },
		doors: { entry: 'closed', bay: 'closed' },
		alarm: { armed: false, triggered: false }
	},
	maintenance: {
		oil_life: 45,
		next_oil_miles: 2500,
		tire_rotation_due: false,
		upcoming: [
			{ service: 'Oil Change', due_miles: 47730, due_date: '2024-03-15' },
			{ service: 'Tire Rotation', due_miles: 50000 }
		]
	},
	network: {
		wifi_clients: 4,
		cellular_signal: -78,
		carrier: 'T-Mobile',
		data_used_gb: 12.5,
		starlink: { connected: true, speed_mbps: 185, obstructions: 2 }
	},
	system: {
		nodes: [
			{ name: 'nav-node', online: true, cpu: 25, memory: 42, temp: 52, disk: 15 },
			{ name: 'net-node', online: true, cpu: 18, memory: 35, temp: 48, disk: 8 },
			{ name: 'nas-node', online: true, cpu: 12, memory: 55, temp: 45, disk: 62 },
			{ name: 'ai-node', online: true, cpu: 45, memory: 68, temp: 58, disk: 22 }
		]
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
