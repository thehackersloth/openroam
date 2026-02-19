/**
 * MQTT Connection Store
 * Handles connection to the MQTT broker and message routing
 */

import { writable, get } from 'svelte/store';
import { roamk, connected } from './roamk';

export interface MqttConfig {
	host: string;
	port: number;
	username?: string;
	password?: string;
	clientId: string;
}

const defaultConfig: MqttConfig = {
	host: 'openroam.local',
	port: 9001, // WebSocket port
	clientId: `openroam-dashboard-${Math.random().toString(16).substr(2, 8)}`
};

export const mqttConfig = writable<MqttConfig>(defaultConfig);
export const mqttStatus = writable<'disconnected' | 'connecting' | 'connected' | 'error'>(
	'disconnected'
);

let client: unknown = null;

// Topic to RoamK path mapping
const topicMap: Record<string, string> = {
	// Power
	'openroam/power/battery/house/voltage': 'power.batteries.house.voltage',
	'openroam/power/battery/house/current': 'power.batteries.house.current',
	'openroam/power/battery/house/soc': 'power.batteries.house.soc',
	'openroam/power/battery/house/temp': 'power.batteries.house.temp',
	'openroam/power/battery/chassis/voltage': 'power.batteries.chassis.voltage',
	'openroam/power/solar/watts': 'power.solar.watts',
	'openroam/power/solar/daily_wh': 'power.solar.daily_wh',
	'openroam/power/shore/connected': 'power.shore.connected',
	'openroam/power/alternator/charging': 'power.alternator.charging',

	// Tanks
	'openroam/tanks/fresh/level': 'tanks.fresh.level',
	'openroam/tanks/fresh/gallons': 'tanks.fresh.gallons',
	'openroam/tanks/grey/level': 'tanks.grey.level',
	'openroam/tanks/black/level': 'tanks.black.level',
	'openroam/tanks/propane/level': 'tanks.propane.level',
	'openroam/tanks/fuel/level': 'tanks.fuel.level',
	'openroam/tanks/fuel/range_miles': 'tanks.fuel.range_miles',

	// Climate
	'openroam/climate/interior/temperature': 'climate.interior.temperature',
	'openroam/climate/interior/humidity': 'climate.interior.humidity',
	'openroam/climate/exterior/temperature': 'climate.exterior.temperature',
	'openroam/climate/hvac/mode': 'climate.hvac.mode',
	'openroam/climate/hvac/running': 'climate.hvac.running',

	// Engine
	'openroam/engine/rpm': 'engine.rpm',
	'openroam/engine/coolant_temp': 'engine.coolant_temp',
	'openroam/engine/oil_temp': 'engine.oil_temp',
	'openroam/engine/throttle': 'engine.throttle',
	'openroam/engine/mpg_instant': 'engine.mpg_instant',
	'openroam/engine/check_engine': 'engine.check_engine',

	// Vehicle
	'openroam/nav/gps/latitude': 'vehicle.location.latitude',
	'openroam/nav/gps/longitude': 'vehicle.location.longitude',
	'openroam/nav/gps/speed': 'vehicle.speed',
	'openroam/nav/gps/heading': 'vehicle.heading',

	// Safety
	'openroam/safety/smoke/status': 'safety.smoke.status',
	'openroam/safety/co/ppm': 'safety.co.ppm',
	'openroam/safety/propane/ppm': 'safety.propane.ppm'
};

export async function connectMqtt() {
	if (typeof window === 'undefined') return;

	const config = get(mqttConfig);
	mqttStatus.set('connecting');

	try {
		// Dynamic import for browser only
		const mqtt = await import('mqtt');

		const url = `ws://${config.host}:${config.port}/mqtt`;

		client = mqtt.connect(url, {
			clientId: config.clientId,
			username: config.username,
			password: config.password,
			reconnectPeriod: 5000
		});

		(client as { on: (event: string, cb: (arg?: unknown) => void) => void }).on(
			'connect',
			() => {
				mqttStatus.set('connected');
				connected.set(true);

				// Subscribe to all openroam topics
				(client as { subscribe: (topic: string) => void }).subscribe('openroam/#');
			}
		);

		(client as { on: (event: string, cb: (topic: string, message: Buffer) => void) => void }).on(
			'message',
			(topic: string, message: Buffer) => {
				const value = parseMessage(message.toString());
				const path = topicMap[topic];

				if (path) {
					roamk.updatePath(path, value);
				}
			}
		);

		(client as { on: (event: string, cb: () => void) => void }).on('close', () => {
			mqttStatus.set('disconnected');
			connected.set(false);
		});

		(client as { on: (event: string, cb: (error: Error) => void) => void }).on(
			'error',
			(error: Error) => {
				console.error('MQTT error:', error);
				mqttStatus.set('error');
			}
		);
	} catch (error) {
		console.error('Failed to connect to MQTT:', error);
		mqttStatus.set('error');
	}
}

export function disconnectMqtt() {
	if (client) {
		(client as { end: () => void }).end();
		client = null;
		mqttStatus.set('disconnected');
		connected.set(false);
	}
}

export function publishMqtt(topic: string, message: string | number | boolean) {
	if (client && get(mqttStatus) === 'connected') {
		(client as { publish: (topic: string, message: string) => void }).publish(
			topic,
			String(message)
		);
	}
}

function parseMessage(message: string): unknown {
	// Try to parse as JSON
	try {
		return JSON.parse(message);
	} catch {
		// Try to parse as number
		const num = parseFloat(message);
		if (!isNaN(num)) return num;

		// Try to parse as boolean
		if (message === 'true') return true;
		if (message === 'false') return false;

		// Return as string
		return message;
	}
}
