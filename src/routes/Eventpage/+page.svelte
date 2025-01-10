<script lang="ts">
    import { page } from '$app/stores'; // Access route parameters
    import { goto } from '$app/navigation'; // For navigation
    import { onMount } from 'svelte';

    let eventId: number;
    let event: any = null;
    let registeredStudents: any[] = [];
    let loading = true;
    let error: string | null = null; // Explicitly typed as string or null

    // Fetch data for the event and registered students
    const fetchEventData = async () => {
    try {
        // Fetch event details
        const eventRes = await fetch(`http://localhost:5000/events/${eventId}`);
        if (!eventRes.ok) throw new Error('Failed to fetch event details');
        event = await eventRes.json();

        // Fetch registered students
        const registrationRes = await fetch(`http://localhost:5000/api/event_registration/${eventId}`);
        if (!registrationRes.ok) throw new Error('Failed to fetch registered students');
        const registrationData = await registrationRes.json();
        registeredStudents = registrationData.registrations; // Access the `registrations` array

        loading = false;
    } catch (err: any) {
        error = err.message;
        loading = false;
    }
};


    // Watch for changes in page and extract eventId from URL
    $: page.subscribe((p) => {
        const id = p.url.searchParams.get('id'); // Extract `id` from query params
        eventId = parseInt(id ?? '0', 10); // Use '0' as fallback if `id` is null
        console.log('Extracted eventId:', eventId);
    });

    // Trigger data fetching if eventId is valid
    $: if (eventId && !isNaN(eventId) && eventId > 0) {
        fetchEventData();
    } else {
        error = 'Invalid or missing eventId';
        loading = false;
    }

    // Back to events main page
    const goBack = () => {
        goto('/Eventmain');
    };
</script>


{#if loading}
    <div>Loading...</div>
{:else}
    {#if error}
        <div class="text-red-500">Error: {error}</div>
    {:else if event && registeredStudents}
        <div>
            <!-- Event Header -->
            <div class="flex items-start p-3 mb-4 bg-gradient-to-r from-[#400000] to-white">
                <button 
                    on:click={goBack} 
                    aria-label="Back to Events"
                    class="mr-4 mt-3 text-orange-400 hover:text-gray-800 transition">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                </button>
                <div>
                    <h1 class="text-2xl font-bold text-white">{event.event_name}</h1>
                    <p class="text-sm text-white mt-1">{event.description}</p>
                </div>
            </div>

            <!-- Event Info -->
            <div class="grid grid-cols-3 gap-2 mb-6 p-3">
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Location</span>
                    <span class="text-gray-600">{event.location}</span>
                </div>
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Date</span>
                    <span class="text-gray-600">{event.event_date}</span>
                </div>
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Time</span>
                    <span class="text-gray-600">{event.start_time} - {event.end_time}</span>
                </div>
                
            </div>

            <!-- Parent Container with Flexbox -->
                <div class="flex gap-4 p-3">
                    <!-- Attendance Info -->
                    <div class="bg-gray-100 p-4 rounded-md flex items-center justify-between w-1/2">
                        <h2 class="text-lg font-semibold text-gray-800">Attendance of Students</h2>
                    </div>

                    <!-- Registered Students Table -->
                    <div class="bg-gray-100 p-3 rounded-md w-1/2">
                        <!-- Registered Students Header -->
                        <h2 class="text-lg font-semibold text-gray-800">Registered Students</h2>
                        <p class="text-2xl font-bold text-orange-400">{registeredStudents.length}</p>

                        <!-- Registered Students Table -->
                        <div class="overflow-x-auto mt-4">
                            <table class="table-auto w-full border-collapse border border-gray-300">
                                <thead>
                                    <tr class="bg-gray-100">
                                        <th class="border border-gray-300 px-4 py-2">Student ID</th>
                                        <th class="border border-gray-300 px-4 py-2">Full Name</th>
                                        <th class="border border-gray-300 px-4 py-2">Year and Block</th>
                                        <th class="border border-gray-300 px-4 py-2">Department</th>
                                        <th class="border border-gray-300 px-4 py-2">Registration Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#each registeredStudents as student}
                                        <tr>
                                            <td class="border border-gray-300 px-4 py-2">{student.student_id}</td>
                                            <td class="border border-gray-300 px-4 py-2">{student.fullname}</td>
                                            <td class="border border-gray-300 px-4 py-2">{student.year_and_block}</td>
                                            <td class="border border-gray-300 px-4 py-2">{student.department}</td>
                                            <td class="border border-gray-300 px-4 py-2">{student.registration_date}</td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
        </div>
    {/if}
{/if}

