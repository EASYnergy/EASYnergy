<script lang="ts">
    import { page } from '$app/stores'; // Access route parameters
    import { goto } from '$app/navigation'; // For navigation
    import { onMount } from 'svelte';

    let eventId: number;
    let event: any = null;
    let registeredStudents: any[] = [];
    let attendanceRecords: any[] = [];
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

         // Fetch attendance records
        const attendanceRes = await fetch(`http://localhost:5000/api/event_attendance/${eventId}`);
        if (!attendanceRes.ok) throw new Error('Failed to fetch attendance records');
        const attendanceData = await attendanceRes.json();
        attendanceRecords = attendanceData.attendance; // Access the `attendance` array

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
            <div class="grid grid-cols-5 gap-2 mb-6 p-3">
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Location</span>
                    <span class="text-gray-600">{event.location}</span>
                </div>
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Date</span>
                    <span class="text-gray-600">{event.event_date}</span>
                </div>
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Start Time</span>
                    <span class="text-gray-600">{event.start_time}</span>
                </div>
                <div class="flex flex-col">
                    <span class="font-medium mb-1">End Time</span>
                    <span class="text-gray-600">{event.end_time}</span>
                </div>
                <div class="flex flex-col">
                    <span class="font-medium mb-1">Speaker</span>
                    <span class="text-gray-600">{event.speaker}</span>
                </div>
                
            </div>

            <!-- Parent Container with Flexbox -->
            <div class="flex gap-4 p-3">

                <!-- Attendance Info -->
                            <div class="bg-gray-100 p-3 rounded-md w-1/2">
                                <div class="flex items-center justify-between">
                                    <h2 class="text-lg font-semibold text-gray-800">Attendance of Students</h2>
                                    <p class="text-2xl font-bold text-orange-400">{attendanceRecords.length}</p>
                                </div>

                                <div class="overflow-x-auto mt-4">
                                    <table class="table-auto w-full border-collapse border border-gray-300 text-left">
                                        <thead>
                                            <tr class="bg-gray-200 text-gray-800">
                                                <th class="border border-gray-300 px-2 py-2">Student ID</th>
                                                <th class="border border-gray-300 px-2 py-2">Full Name</th>
                                                <th class="border border-gray-300 px-2 py-2">Year and Block</th>
                                                <th class="border border-gray-300 px-2 py-2">Department</th>
                                                <th class="border border-gray-300 px-2 py-2">Check-in</th>
                                                <th class="border border-gray-300 px-2 py-2">Check-out</th>
                                                <th class="border border-gray-300 px-2 py-2">Status</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {#if attendanceRecords.length > 0}
                                                {#each attendanceRecords as record}
                                                    <tr class="hover:bg-gray-100">
                                                        <td class="border border-gray-300 px-4 py-2">{record.student_id}</td>
                                                        <td class="border border-gray-300 px-4 py-2">{record.fullname}</td>
                                                        <td class="border border-gray-300 px-4 py-2">{record.year_and_block}</td>
                                                        <td class="border border-gray-300 px-4 py-2">{record.department}</td>
                                                        <td class="border border-gray-300 px-4 py-2">{record.check_in || 'N/A'}</td>
                                                        <td class="border border-gray-300 px-4 py-2">{record.check_out || 'N/A'}</td>
                                                        <td class="border border-gray-300 px-4 py-2">{record.status}</td>
                                                    </tr>
                                                {/each}
                                            {:else}
                                                <tr>
                                                    <td colspan="7" class="border border-gray-300 px-4 py-2 text-center text-gray-500">
                                                        No attendance records found.
                                                    </td>
                                                </tr>
                                            {/if}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

            
                <!-- Registered Students Table -->
                    <div class="bg-gray-100 p-3 rounded-md w-1/2">
                        <div class="flex items-center justify-between">
                            <h2 class="text-lg font-semibold text-gray-800">Registered Students</h2>
                            <p class="text-2xl font-bold text-orange-400">{registeredStudents.length}</p>
                        </div>

                        <div class="overflow-x-auto mt-4">
                            <table class="table-auto w-full border-collapse border border-gray-300 text-left">
                                <thead>
                                    <tr class="bg-gray-200 text-gray-800">
                                        <th class="border border-gray-300 px-3 py-2">Student ID</th>
                                        <th class="border border-gray-300 px-3 py-2">Full Name</th>
                                        <th class="border border-gray-300 px-3 py-2">Year and Block</th>
                                        <th class="border border-gray-300 px-3 py-2">Department</th>
                                        <th class="border border-gray-300 px-3 py-2">Registration Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#if registeredStudents.length > 0}
                                        {#each registeredStudents as student}
                                            <tr class="hover:bg-gray-100">
                                                <td class="border border-gray-300 px-4 py-2">{student.student_id}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.fullname}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.year_and_block}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.department}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.registration_date || 'N/A'}</td>
                                            </tr>
                                        {/each}
                                    {:else}
                                        <tr>
                                            <td colspan="5" class="border border-gray-300 px-4 py-2 text-center text-gray-500">
                                                No registered students found.
                                            </td>
                                        </tr>
                                    {/if}
                                </tbody>
                            </table>
                        </div>
                    </div>
            </div>   
        </div>
    {/if}
{/if}

