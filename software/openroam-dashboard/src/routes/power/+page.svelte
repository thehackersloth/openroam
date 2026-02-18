<script lang="ts">
	import { roamk, power } from '$lib/stores/roamk';

	function getBatteryColor(soc: number): string {
		if (soc > 50) return 'text-green-400';
		if (soc > 20) return 'text-yellow-400';
		return 'text-red-400';
	}

	function getCurrentColor(current: number): string {
		if (current > 0) return 'text-green-400';
		if (current < -20) return 'text-red-400';
		return 'text-yellow-400';
	}
</script>

<div class="space-y-6">
	<h1 class="text-2xl font-bold">Power Management</h1>

	<!-- Battery Banks -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		<!-- House Battery -->
		<div class="card">
			<div class="card-header">House Battery</div>
			<div class="text-center py-4">
				<div class="gauge-value {getBatteryColor($power.batteries.house?.soc ?? 0)}">
					{$power.batteries.house?.soc ?? 0}%
				</div>
				<div class="gauge-label">State of Charge</div>
			</div>
			<div class="grid grid-cols-2 gap-4 text-sm">
				<div>
					<div class="text-gray-400">Voltage</div>
					<div class="font-medium">{($power.batteries.house?.voltage ?? 0).toFixed(2)}V</div>
				</div>
				<div>
					<div class="text-gray-400">Current</div>
					<div class="font-medium {getCurrentColor($power.batteries.house?.current ?? 0)}">
						{($power.batteries.house?.current ?? 0).toFixed(1)}A
					</div>
				</div>
				<div>
					<div class="text-gray-400">Temperature</div>
					<div class="font-medium">{$power.batteries.house?.temp ?? 0}°F</div>
				</div>
				<div>
					<div class="text-gray-400">Capacity</div>
					<div class="font-medium">{$power.batteries.house?.capacity_ah ?? 0}Ah</div>
				</div>
			</div>
		</div>

		<!-- Chassis Battery -->
		<div class="card">
			<div class="card-header">Chassis Battery</div>
			<div class="text-center py-4">
				<div class="gauge-value {getBatteryColor($power.batteries.chassis?.soc ?? 0)}">
					{$power.batteries.chassis?.soc ?? 0}%
				</div>
				<div class="gauge-label">State of Charge</div>
			</div>
			<div class="grid grid-cols-2 gap-4 text-sm">
				<div>
					<div class="text-gray-400">Voltage</div>
					<div class="font-medium">{($power.batteries.chassis?.voltage ?? 0).toFixed(2)}V</div>
				</div>
				<div>
					<div class="text-gray-400">Current</div>
					<div class="font-medium">{($power.batteries.chassis?.current ?? 0).toFixed(1)}A</div>
				</div>
			</div>
		</div>

		<!-- Solar -->
		<div class="card">
			<div class="card-header">Solar</div>
			<div class="text-center py-4">
				<div class="gauge-value text-yellow-400">
					{$power.solar.watts}W
				</div>
				<div class="gauge-label">Current Production</div>
			</div>
			<div class="grid grid-cols-2 gap-4 text-sm">
				<div>
					<div class="text-gray-400">Voltage</div>
					<div class="font-medium">{$power.solar.voltage.toFixed(1)}V</div>
				</div>
				<div>
					<div class="text-gray-400">Current</div>
					<div class="font-medium">{$power.solar.current.toFixed(1)}A</div>
				</div>
				<div>
					<div class="text-gray-400">Today</div>
					<div class="font-medium">{$power.solar.daily_wh}Wh</div>
				</div>
				<div>
					<div class="text-gray-400">Lifetime</div>
					<div class="font-medium">{($power.solar.lifetime_kwh ?? 0).toFixed(1)}kWh</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Shore Power & Alternator -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
		<div class="card">
			<div class="card-header">Shore Power</div>
			<div class="flex items-center gap-4">
				<div class="w-16 h-16 rounded-full flex items-center justify-center {$power.shore.connected ? 'bg-green-600/20' : 'bg-gray-700'}">
					<span class="text-2xl">🔌</span>
				</div>
				<div>
					<div class="font-medium text-lg">
						{$power.shore.connected ? 'Connected' : 'Disconnected'}
					</div>
					{#if $power.shore.connected}
						<div class="text-sm text-gray-400">
							{$power.shore.voltage}V @ {$power.shore.amps}A
						</div>
					{/if}
				</div>
			</div>
		</div>

		<div class="card">
			<div class="card-header">Alternator</div>
			<div class="flex items-center gap-4">
				<div class="w-16 h-16 rounded-full flex items-center justify-center {$power.alternator.charging ? 'bg-green-600/20' : 'bg-gray-700'}">
					<span class="text-2xl">🔄</span>
				</div>
				<div>
					<div class="font-medium text-lg">
						{$power.alternator.charging ? 'Charging' : 'Not Charging'}
					</div>
					{#if $power.alternator.charging}
						<div class="text-sm text-gray-400">
							{$power.alternator.amps}A
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>

	<!-- Power Flow Diagram -->
	<div class="card">
		<div class="card-header">Power Flow</div>
		<div class="flex items-center justify-center gap-8 py-8 text-center">
			<!-- Sources -->
			<div class="space-y-4">
				<div class="p-4 rounded-lg bg-yellow-600/20">
					<div class="text-2xl mb-1">☀️</div>
					<div class="text-sm">Solar</div>
					<div class="font-bold text-yellow-400">{$power.solar.watts}W</div>
				</div>
				{#if $power.shore.connected}
					<div class="p-4 rounded-lg bg-blue-600/20">
						<div class="text-2xl mb-1">🔌</div>
						<div class="text-sm">Shore</div>
						<div class="font-bold text-blue-400">{$power.shore.voltage * $power.shore.amps}W</div>
					</div>
				{/if}
				{#if $power.alternator.charging}
					<div class="p-4 rounded-lg bg-green-600/20">
						<div class="text-2xl mb-1">🔄</div>
						<div class="text-sm">Alternator</div>
						<div class="font-bold text-green-400">{($power.batteries.house?.voltage ?? 12) * $power.alternator.amps}W</div>
					</div>
				{/if}
			</div>

			<!-- Arrow -->
			<div class="text-4xl text-gray-500">→</div>

			<!-- Battery -->
			<div class="p-6 rounded-lg bg-roam-600/20">
				<div class="text-4xl mb-2">🔋</div>
				<div class="text-sm">House Battery</div>
				<div class="gauge-value {getBatteryColor($power.batteries.house?.soc ?? 0)}">
					{$power.batteries.house?.soc ?? 0}%
				</div>
			</div>

			<!-- Arrow -->
			<div class="text-4xl text-gray-500">→</div>

			<!-- Loads -->
			<div class="p-4 rounded-lg bg-purple-600/20">
				<div class="text-2xl mb-1">💡</div>
				<div class="text-sm">Loads</div>
				<div class="font-bold text-purple-400">
					{Math.abs(($power.batteries.house?.current ?? 0) * ($power.batteries.house?.voltage ?? 12)).toFixed(0)}W
				</div>
			</div>
		</div>
	</div>
</div>
