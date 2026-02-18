<script lang="ts">
	import { tanks } from '$lib/stores/roamk';
	import { publishMqtt } from '$lib/stores/mqtt';

	const tankConfig = {
		fresh: { label: 'Fresh Water', color: 'bg-blue-500', icon: '💧', capacity: 40 },
		grey: { label: 'Grey Water', color: 'bg-gray-500', icon: '🚿', capacity: 40 },
		black: { label: 'Black Water', color: 'bg-amber-800', icon: '🚽', capacity: 40 },
		propane: { label: 'Propane', color: 'bg-orange-500', icon: '🔥', capacity: 30 },
		fuel: { label: 'Fuel', color: 'bg-emerald-500', icon: '⛽', capacity: 50 }
	};

	function getLevelColor(level: number, tankType: string): string {
		if (tankType === 'fresh' || tankType === 'propane' || tankType === 'fuel') {
			// Low is bad
			if (level < 20) return 'text-red-400';
			if (level < 40) return 'text-yellow-400';
			return 'text-green-400';
		} else {
			// High is bad (grey/black)
			if (level > 80) return 'text-red-400';
			if (level > 60) return 'text-yellow-400';
			return 'text-green-400';
		}
	}

	function togglePump() {
		publishMqtt('openroam/tanks/pump/command', 'toggle');
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-2xl font-bold">Tank Levels</h1>
		<button class="btn btn-primary" on:click={togglePump}>
			💧 Toggle Water Pump
		</button>
	</div>

	<!-- Tank Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		{#each Object.entries($tanks) as [key, tank]}
			{@const config = tankConfig[key as keyof typeof tankConfig]}
			<div class="card">
				<div class="card-header flex items-center gap-2">
					<span>{config.icon}</span>
					<span>{config.label}</span>
				</div>

				<!-- Visual Tank -->
				<div class="relative h-48 bg-gray-700 rounded-lg overflow-hidden my-4">
					<div
						class="absolute bottom-0 left-0 right-0 {config.color} transition-all duration-500"
						style="height: {tank.level}%"
					>
						<!-- Wave effect -->
						<div class="absolute top-0 left-0 right-0 h-4 bg-white/10"></div>
					</div>
					<div class="absolute inset-0 flex items-center justify-center">
						<div class="text-center">
							<div class="gauge-value {getLevelColor(tank.level, key)}">
								{tank.level}%
							</div>
						</div>
					</div>
				</div>

				<!-- Details -->
				<div class="grid grid-cols-2 gap-4 text-sm">
					<div>
						<div class="text-gray-400">Current</div>
						<div class="font-medium">
							{tank.gallons ?? Math.round((tank.level / 100) * config.capacity)} gal
						</div>
					</div>
					<div>
						<div class="text-gray-400">Capacity</div>
						<div class="font-medium">{tank.capacity ?? config.capacity} gal</div>
					</div>
					{#if key === 'fuel' && tank.range_miles}
						<div class="col-span-2">
							<div class="text-gray-400">Range</div>
							<div class="font-medium text-lg">{tank.range_miles} miles</div>
						</div>
					{/if}
					{#if key === 'propane' && tank.pounds}
						<div class="col-span-2">
							<div class="text-gray-400">Weight</div>
							<div class="font-medium text-lg">{tank.pounds} lbs</div>
						</div>
					{/if}
				</div>
			</div>
		{/each}
	</div>

	<!-- Tank Alerts -->
	<div class="card">
		<div class="card-header">Alerts & Reminders</div>
		<div class="space-y-2">
			{#if $tanks.fresh.level < 20}
				<div class="p-3 bg-red-600/20 rounded-lg text-red-400">
					⚠️ Fresh water low - consider refilling soon
				</div>
			{/if}
			{#if $tanks.grey.level > 80}
				<div class="p-3 bg-yellow-600/20 rounded-lg text-yellow-400">
					⚠️ Grey water high - consider dumping soon
				</div>
			{/if}
			{#if $tanks.black.level > 75}
				<div class="p-3 bg-yellow-600/20 rounded-lg text-yellow-400">
					⚠️ Black water high - consider dumping soon
				</div>
			{/if}
			{#if $tanks.propane.level < 25}
				<div class="p-3 bg-orange-600/20 rounded-lg text-orange-400">
					⚠️ Propane low - refill recommended
				</div>
			{/if}
			{#if $tanks.fuel.level < 25}
				<div class="p-3 bg-red-600/20 rounded-lg text-red-400">
					⚠️ Fuel low - find a gas station
				</div>
			{/if}
			{#if $tanks.fresh.level >= 20 && $tanks.grey.level <= 80 && $tanks.black.level <= 75 && $tanks.propane.level >= 25 && $tanks.fuel.level >= 25}
				<div class="p-3 bg-green-600/20 rounded-lg text-green-400">
					✓ All tank levels normal
				</div>
			{/if}
		</div>
	</div>
</div>
