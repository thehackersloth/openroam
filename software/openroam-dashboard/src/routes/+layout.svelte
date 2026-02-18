<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { connected, roamk } from '$lib/stores/roamk';
	import { connectMqtt, mqttStatus } from '$lib/stores/mqtt';
	import { onMount } from 'svelte';

	// Navigation items
	const navItems = [
		{ path: '/', label: 'Dashboard', icon: '🏠' },
		{ path: '/power', label: 'Power', icon: '⚡' },
		{ path: '/tanks', label: 'Tanks', icon: '💧' },
		{ path: '/climate', label: 'Climate', icon: '🌡️' },
		{ path: '/vehicle', label: 'Vehicle', icon: '🚐' },
		{ path: '/engine', label: 'Engine', icon: '🔧' },
		{ path: '/maintenance', label: 'Maintenance', icon: '📋' },
		{ path: '/cameras', label: 'Cameras', icon: '📷' },
		{ path: '/media', label: 'Media', icon: '🎵' },
		{ path: '/radio', label: 'Radio', icon: '📻' },
		{ path: '/system', label: 'System', icon: '⚙️' }
	];

	let sidebarOpen = true;

	onMount(() => {
		connectMqtt();
	});

	$: currentPath = $page.url.pathname;
</script>

<div class="flex h-screen overflow-hidden">
	<!-- Sidebar -->
	<aside
		class="w-64 bg-gray-800 border-r border-gray-700 flex flex-col {sidebarOpen
			? ''
			: 'hidden lg:flex'}"
	>
		<!-- Logo -->
		<div class="p-4 border-b border-gray-700">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-roam-600 rounded-lg flex items-center justify-center">
					<span class="text-xl">🚐</span>
				</div>
				<div>
					<h1 class="font-bold text-lg">OpenRoam</h1>
					<div class="flex items-center gap-2 text-xs">
						{#if $connected}
							<span class="w-2 h-2 bg-green-500 rounded-full"></span>
							<span class="text-green-400">Connected</span>
						{:else}
							<span class="w-2 h-2 bg-red-500 rounded-full"></span>
							<span class="text-red-400">Disconnected</span>
						{/if}
					</div>
				</div>
			</div>
		</div>

		<!-- Navigation -->
		<nav class="flex-1 overflow-y-auto p-2">
			{#each navItems as item}
				<a
					href={item.path}
					class="nav-link {currentPath === item.path ? 'active' : ''}"
				>
					<span class="text-lg">{item.icon}</span>
					<span>{item.label}</span>
				</a>
			{/each}
		</nav>

		<!-- Footer status -->
		<div class="p-4 border-t border-gray-700 text-xs text-gray-500">
			<div class="flex justify-between">
				<span>MQTT: {$mqttStatus}</span>
				<span>v0.1.0</span>
			</div>
		</div>
	</aside>

	<!-- Main content -->
	<main class="flex-1 overflow-y-auto">
		<!-- Top bar -->
		<header class="bg-gray-800 border-b border-gray-700 px-4 py-3 flex items-center justify-between">
			<button
				class="lg:hidden p-2 hover:bg-gray-700 rounded"
				on:click={() => (sidebarOpen = !sidebarOpen)}
			>
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
				</svg>
			</button>

			<!-- Quick stats -->
			<div class="flex items-center gap-6 text-sm">
				<div class="flex items-center gap-2">
					<span class="text-gray-400">🔋</span>
					<span class="font-medium">{$roamk.power.batteries.house?.soc ?? 0}%</span>
				</div>
				<div class="flex items-center gap-2">
					<span class="text-gray-400">☀️</span>
					<span class="font-medium">{$roamk.power.solar.watts ?? 0}W</span>
				</div>
				<div class="flex items-center gap-2">
					<span class="text-gray-400">💧</span>
					<span class="font-medium">{$roamk.tanks.fresh.level ?? 0}%</span>
				</div>
				<div class="flex items-center gap-2">
					<span class="text-gray-400">🌡️</span>
					<span class="font-medium">{$roamk.climate.interior.temperature ?? 0}°</span>
				</div>
			</div>

			<!-- Time and date -->
			<div class="text-sm text-gray-400">
				{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
			</div>
		</header>

		<!-- Page content -->
		<div class="p-4">
			<slot />
		</div>
	</main>
</div>
