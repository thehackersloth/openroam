<script lang="ts">
	import { roamk } from '$lib/stores/roamk';

	// Tank colors
	const tankColors: Record<string, string> = {
		fresh: 'bg-blue-500',
		grey: 'bg-gray-500',
		black: 'bg-amber-800',
		propane: 'bg-orange-500',
		fuel: 'bg-emerald-500'
	};

	// Battery status color
	function getBatteryColor(soc: number): string {
		if (soc > 50) return 'text-green-400';
		if (soc > 20) return 'text-yellow-400';
		return 'text-red-400';
	}

	// Safety status
	$: safetyStatus = (() => {
		if ($roamk.safety.smoke.status === 'alarm') return { text: 'SMOKE ALARM', color: 'bg-red-600' };
		if ($roamk.safety.co.status === 'alarm') return { text: 'CO ALARM', color: 'bg-red-600' };
		if ($roamk.safety.propane.status === 'alarm') return { text: 'GAS LEAK', color: 'bg-red-600' };
		return { text: 'All Clear', color: 'bg-green-600' };
	})();
</script>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<h1 class="text-2xl font-bold">Dashboard</h1>
		<div class="text-sm text-gray-400">
			Last update: {new Date($roamk.lastUpdate).toLocaleTimeString()}
		</div>
	</div>

	<!-- Safety Alert -->
	{#if safetyStatus.text !== 'All Clear'}
		<div class="p-4 rounded-lg {safetyStatus.color} text-white font-bold text-center animate-pulse">
			⚠️ {safetyStatus.text}
		</div>
	{/if}

	<!-- Main Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		<!-- Power Card -->
		<div class="card">
			<div class="card-header">Power</div>
			<div class="space-y-4">
				<!-- House Battery -->
				<div class="flex items-center justify-between">
					<div>
						<div class="text-sm text-gray-400">House Battery</div>
						<div class="gauge-value {getBatteryColor($roamk.power.batteries.house?.soc ?? 0)}">
							{$roamk.power.batteries.house?.soc ?? 0}%
						</div>
					</div>
					<div class="text-right text-sm">
						<div>{($roamk.power.batteries.house?.voltage ?? 0).toFixed(1)}V</div>
						<div class="{$roamk.power.batteries.house?.current ?? 0 > 0 ? 'text-green-400' : 'text-red-400'}">
							{($roamk.power.batteries.house?.current ?? 0).toFixed(1)}A
						</div>
					</div>
				</div>

				<!-- Solar -->
				<div class="flex items-center justify-between">
					<div>
						<div class="text-sm text-gray-400">Solar</div>
						<div class="text-2xl font-bold text-yellow-400">
							{$roamk.power.solar.watts}W
						</div>
					</div>
					<div class="text-right text-sm">
						<div>{$roamk.power.solar.daily_wh}Wh today</div>
					</div>
				</div>

				<!-- Shore Power -->
				<div class="flex items-center gap-2 text-sm">
					<span class="w-2 h-2 rounded-full {$roamk.power.shore.connected ? 'bg-green-500' : 'bg-gray-500'}"></span>
					<span>Shore: {$roamk.power.shore.connected ? 'Connected' : 'Disconnected'}</span>
				</div>
			</div>
			<a href="/power" class="block mt-4 text-sm text-roam-400 hover:text-roam-300">
				View Details →
			</a>
		</div>

		<!-- Tanks Card -->
		<div class="card">
			<div class="card-header">Tanks</div>
			<div class="space-y-3">
				{#each Object.entries($roamk.tanks) as [name, tank]}
					<div>
						<div class="flex justify-between text-sm mb-1">
							<span class="capitalize">{name}</span>
							<span>{tank.level}%</span>
						</div>
						<div class="tank-bar">
							<div
								class="tank-fill {tankColors[name]}"
								style="width: {tank.level}%"
							></div>
						</div>
					</div>
				{/each}
			</div>
			<a href="/tanks" class="block mt-4 text-sm text-roam-400 hover:text-roam-300">
				View Details →
			</a>
		</div>

		<!-- Climate Card -->
		<div class="card">
			<div class="card-header">Climate</div>
			<div class="grid grid-cols-2 gap-4">
				<div class="text-center">
					<div class="text-sm text-gray-400">Interior</div>
					<div class="gauge-value">{$roamk.climate.interior.temperature}°</div>
					<div class="text-sm text-gray-400">{$roamk.climate.interior.humidity}% RH</div>
				</div>
				<div class="text-center">
					<div class="text-sm text-gray-400">Exterior</div>
					<div class="text-2xl font-bold">{$roamk.climate.exterior.temperature}°</div>
				</div>
			</div>
			<div class="mt-4 flex items-center justify-between text-sm">
				<span>HVAC: {$roamk.climate.hvac.mode}</span>
				<span class="{$roamk.climate.hvac.running ? 'text-green-400' : 'text-gray-400'}">
					{$roamk.climate.hvac.running ? 'Running' : 'Idle'}
				</span>
			</div>
			<a href="/climate" class="block mt-4 text-sm text-roam-400 hover:text-roam-300">
				View Details →
			</a>
		</div>

		<!-- Location Card -->
		<div class="card">
			<div class="card-header">Location</div>
			<div class="space-y-2">
				<div class="flex items-center gap-2">
					<span class="text-2xl">📍</span>
					<div>
						<div class="font-medium">
							{$roamk.vehicle.location.latitude.toFixed(4)}°,
							{$roamk.vehicle.location.longitude.toFixed(4)}°
						</div>
						<div class="text-sm text-gray-400">
							{$roamk.vehicle.location.altitude ?? 0}m elevation
						</div>
					</div>
				</div>
				<div class="grid grid-cols-2 gap-4 text-center mt-4">
					<div>
						<div class="text-sm text-gray-400">Speed</div>
						<div class="text-xl font-bold">{$roamk.vehicle.speed} mph</div>
					</div>
					<div>
						<div class="text-sm text-gray-400">Heading</div>
						<div class="text-xl font-bold">{$roamk.vehicle.heading}°</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Engine Card -->
		<div class="card">
			<div class="card-header">Engine</div>
			<div class="space-y-4">
				<div class="grid grid-cols-2 gap-4">
					<div class="text-center">
						<div class="text-sm text-gray-400">RPM</div>
						<div class="text-2xl font-bold">{$roamk.engine.rpm}</div>
					</div>
					<div class="text-center">
						<div class="text-sm text-gray-400">Coolant</div>
						<div class="text-2xl font-bold">{$roamk.engine.coolant_temp}°</div>
					</div>
				</div>
				<div class="flex items-center justify-between text-sm">
					<span>Oil Temp: {$roamk.engine.oil_temp}°</span>
					<span>MPG: {$roamk.engine.mpg_instant.toFixed(1)}</span>
				</div>
				{#if $roamk.engine.check_engine}
					<div class="p-2 bg-yellow-600/20 rounded text-yellow-400 text-sm text-center">
						⚠️ Check Engine Light
					</div>
				{/if}
			</div>
			<a href="/engine" class="block mt-4 text-sm text-roam-400 hover:text-roam-300">
				View Details →
			</a>
		</div>

		<!-- Safety Card -->
		<div class="card">
			<div class="card-header">Safety</div>
			<div class="space-y-3">
				<div class="flex items-center justify-between">
					<span>Smoke</span>
					<span class="{$roamk.safety.smoke.status === 'ok' ? 'status-ok' : 'status-error'}">
						{$roamk.safety.smoke.status.toUpperCase()}
					</span>
				</div>
				<div class="flex items-center justify-between">
					<span>CO</span>
					<span class="{$roamk.safety.co.status === 'ok' ? 'status-ok' : 'status-error'}">
						{$roamk.safety.co.ppm} ppm
					</span>
				</div>
				<div class="flex items-center justify-between">
					<span>Propane</span>
					<span class="{$roamk.safety.propane.status === 'ok' ? 'status-ok' : 'status-error'}">
						{$roamk.safety.propane.ppm} ppm
					</span>
				</div>
				<div class="flex items-center justify-between">
					<span>Alarm</span>
					<span class="{$roamk.safety.alarm.armed ? 'text-yellow-400' : 'text-gray-400'}">
						{$roamk.safety.alarm.armed ? 'Armed' : 'Disarmed'}
					</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Maintenance Reminder -->
	{#if $roamk.maintenance.upcoming.length > 0}
		<div class="card">
			<div class="card-header">Upcoming Maintenance</div>
			<div class="divide-y divide-gray-700">
				{#each $roamk.maintenance.upcoming.slice(0, 3) as item}
					<div class="py-2 flex items-center justify-between">
						<span>{item.service}</span>
						<span class="text-sm text-gray-400">
							{item.due_miles ? `${item.due_miles} mi` : item.due_date}
						</span>
					</div>
				{/each}
			</div>
			<a href="/maintenance" class="block mt-4 text-sm text-roam-400 hover:text-roam-300">
				View All →
			</a>
		</div>
	{/if}
</div>
