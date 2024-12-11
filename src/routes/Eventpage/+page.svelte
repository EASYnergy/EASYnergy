<script lang="ts">
    import { goto } from '$app/navigation';

    // Placeholder data to simulate fetched data
    let event = {
        name: "Tech Summit 2024",
        description: "A gathering for tech enthusiasts to discuss emerging technologies.",
        date: "2024-12-20",
        location: "Gordon College Auditorium",
        time: "10:00 AM - 4:00 PM",
        attendance: {
            attended: 120,
            registered: 200
        }
    };

    // Back to events main page
    const goBack = () => {
        goto('/Eventmain');
    };
</script>

<div class="">
    <div class="flex items-start p-3 mb-4 bg-gradient-to-r from-[#400000] to-white">
        <!-- Back Button with aria-label -->
        <button 
            on:click={goBack} 
            aria-label="Back to Events"
            class="mr-4 mt-3 text-orange-400  hover:text-gray-800 transition"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
        </button>

        <div>
            <!-- Event Title -->
            <h1 class="text-2xl font-bold text-white">{event.name}</h1>
            
            <!-- Description -->
            <p class="text-sm text-white mt-1">{event.description}</p>
        </div>
    </div>


    <!-- Location, Date, Time Row -->
    <div class="grid grid-cols-3 gap-2 mb-6 p-3 ">
        <div class="flex flex-col">
            <span class="font-medium mb-1">Location</span>
            <span class="text-gray-600">{event.location}</span>
        </div>
        <div class="flex flex-col">
            <span class="font-medium mb-1">Date</span>
            <span class="text-gray-600">{event.date}</span>
        </div>
        <div class="flex flex-col">
            <span class="font-medium mb-1">Time</span>
            <span class="text-gray-600">{event.time}</span>
        </div>
    </div>

    <!-- Attendance Columns -->
    <div class="grid grid-cols-2 gap-2 p-3">
        <div class="bg-gray-100 p-4 rounded-md flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-800">Registered Students</h2>
            <p class="text-2xl font-bold text-orange-400 ">{event.attendance.registered}</p>
        </div>
        
        <div class="bg-gray-100 p-4 rounded-md flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-800">Students Attended</h2>
            <p class="text-2xl font-bold text-orange-400 ">{event.attendance.attended}</p>
        </div>
    </div>
</div>