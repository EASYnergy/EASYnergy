<script lang="ts">
    import { onMount } from 'svelte';
    import Header from '../Header/+page.svelte'; // Import Header component

    let userName: string = "John Doe"; // Example user name
    let miniPfpClicked = false; // Track whether the mini profile picture is clicked
    let searchQuery: string = ""; // Bind to the search input
    let filteredEvents = []; // Store filtered events

    // Sample event data
    let events = [
        { id: 1, name: "Tech Conference", date: "2024-12-15", location: "GCCCS Hall", description: "A conference on the latest in technology." },
        { id: 2, name: "Coding Workshop", date: "2024-12-18", location: "Room 101", description: "A hands-on workshop on full-stack development." },
        { id: 3, name: "Networking Event", date: "2024-12-20", location: "Online", description: "A virtual networking event for students and professionals." }
    ];

    // Simulate fetching events from a database
    const fetchEvents = async () => {
        console.log("Fetching events...");
        // Simulate a database call or API fetch
        // events = await fetch('/api/events');
    };

    // Function to toggle the sidebar visibility
    const toggleSidebar = () => {
        miniPfpClicked = !miniPfpClicked;
    };

    // Filter events based on search query
    $: filteredEvents = events.filter(event =>
        event.name.toLowerCase().startsWith(searchQuery.toLowerCase())
    );

    // Event functions
    const viewEventDetails = (eventId: number) => {
        console.log(`Viewing details for event ID: ${eventId}`);
        // Implement routing logic or modal opening
    };

    const deleteEvent = (eventId: number) => {
        console.log(`Deleting event ID: ${eventId}`);
        // Implement delete logic here
    };

    onMount(() => {
        fetchEvents();
    });
</script>


<Header /> <!-- Render the Header component -->

<style>
    /* Additional styles can go here */
</style>

<div class="bg-transparent fixed top-0 w-full p-4 z-10">
    <div class="flex flex-col items-center p-6 rounded-lg">
        
        <!-- Search Bar and Create Event Button -->
        <div class="w-full flex items-center mb-6 mt-[100px]">
           <!-- Search Bar -->
    <input
    type="text"
    placeholder="Search events..."
    class="w-full sm:w-2/3 md:w-3/4 px-4 py-2 bg-gray-100 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500"
    bind:value={searchQuery}
/>
            
            <!-- Create Event Button -->
            <button class="ml-4 bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600 transition-all" on:click={() => console.log("Creating a new event...")}>Create Event</button>
        </div>

        <!-- Event List -->
        <div class="w-full">
            <table class="w-full table-auto">
                <thead>
                    <tr>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Event Name</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Description</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Date</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Location</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">View</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Delete</th>
                    </tr>
                </thead>
                <tbody>
                    {#each events as event}
                        <tr class="hover:bg-gray-100">
                            <td class="py-2 px-4">{event.name}</td>
                            <td class="py-2 px-4">{event.description}</td>
                            <td class="py-2 px-4">{event.date}</td>
                            <td class="py-2 px-4">{event.location}</td>
                            <td class="py-2 px-4">
                                <button class="bg-blue-500 text-white py-1 px-4 rounded-md hover:bg-blue-600" on:click={() => viewEventDetails(event.id)}>View</button>
                            </td>
                            <td class="py-2 px-4">
                                <button class="bg-red-500 text-white py-1 px-4 rounded-md hover:bg-red-600" on:click={() => deleteEvent(event.id)}>Delete</button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>
